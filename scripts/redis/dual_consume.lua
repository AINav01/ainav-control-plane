-- AINav Control Plane — dual (N-role) token consume
-- Atomic validate-all-then-write-all for multi-host admit.
--
-- KEYS[1]    = request hash key   e.g. ainav:req:{request_id}
-- KEYS[2..N] = token hash keys    e.g. ainav:tok:{request_id}:{token_id}
-- ARGV[1]    = expected action_hash (canonicalized in app)
-- ARGV[2]    = now (unix seconds)
--
-- Returns: {ok='executed'} | {err='<code>'}
-- Docs: docs/REDIS_LUA_DUAL_ADMIT.md

local function hget(key, field, default)
  local v = redis.call('HGET', key, field)
  if v == false then
    return default
  end
  return v
end

if #KEYS < 2 then
  return redis.error_reply('numkeys must be >= 2 (request + tokens)')
end

if redis.call('EXISTS', KEYS[1]) == 0 then
  return {err = 'unknown_request'}
end

if hget(KEYS[1], 'consumed', '0') == '1' then
  return {err = 'already_consumed'}
end

if hget(KEYS[1], 'revoked', '0') == '1' then
  return {err = 'revoked'}
end

local exp = tonumber(hget(KEYS[1], 'expires', '0'))
if exp and exp > 0 and tonumber(ARGV[2]) > exp then
  return {err = 'expired'}
end

if hget(KEYS[1], 'action_hash', '') ~= ARGV[1] then
  return {err = 'hash_mismatch'}
end

for i = 2, #KEYS do
  local tk = KEYS[i]
  if redis.call('EXISTS', tk) == 0 then
    return {err = 'missing_token'}
  end
  if hget(tk, 'used', '0') == '1' then
    return {err = 'token_used'}
  end
  local texp = tonumber(hget(tk, 'expires', '0'))
  if texp and texp > 0 and tonumber(ARGV[2]) > texp then
    return {err = 'token_expired'}
  end
  if hget(tk, 'action_hash', '') ~= ARGV[1] then
    return {err = 'token_hash_mismatch'}
  end
end

for i = 2, #KEYS do
  redis.call('HSET', KEYS[i], 'used', '1', 'used_at', ARGV[2])
end
redis.call('HSET', KEYS[1], 'consumed', '1', 'consumed_at', ARGV[2])

return {ok = 'executed'}
