-- AINav Control Plane — dual (N-role) token consume
-- Atomic validate-all-then-write-all for multi-host admit.
--
-- KEYS[1]    = request HASH   e.g. ainav:req:{request_id}
-- KEYS[2..N] = token HASHes   e.g. ainav:tok:{request_id}:{token_id}
-- ARGV[1]    = expected action_hash (canonicalized in app; must match stored)
-- ARGV[2]    = now (unix seconds) for expiry checks
--
-- Request HASH fields (required unless noted):
--   request_id, action_hash, consumed, revoked, expires_at
--   required_n (optional) — if set, must equal #KEYS-1
--
-- Token HASH fields:
--   request_id, action_hash, role, principal, used, expires_at
--
-- Returns: {ok='executed', n='<token_count>'} | {err='<code>'}
-- Docs: docs/REDIS_LUA_DUAL_ADMIT.md
--
-- Design: fail-closed, no writes until every predicate passes.
-- Do not put policy/OPA/canonical JSON/SoR I/O in this script.

local function hget(key, field, default)
  local v = redis.call('HGET', key, field)
  if v == false then
    return default
  end
  return v
end

local function expires_field(key)
  -- Prefer expires_at (lab/product); accept expires for older seeds
  local v = redis.call('HGET', key, 'expires_at')
  if v == false then
    v = redis.call('HGET', key, 'expires')
  end
  if v == false then
    return 0
  end
  return tonumber(v) or 0
end

if #KEYS < 2 then
  return redis.error_reply('numkeys must be >= 2 (request + at least one token)')
end

if ARGV[1] == false or ARGV[1] == nil or ARGV[1] == '' then
  return {err = 'missing_expected_hash'}
end

if ARGV[2] == false or ARGV[2] == nil or ARGV[2] == '' then
  return {err = 'missing_now'}
end

local now = tonumber(ARGV[2])
if not now then
  return {err = 'invalid_now'}
end

local req = KEYS[1]

if redis.call('EXISTS', req) == 0 then
  return {err = 'unknown_request'}
end

if hget(req, 'consumed', '0') == '1' then
  return {err = 'already_consumed'}
end

if hget(req, 'revoked', '0') == '1' then
  return {err = 'revoked'}
end

local req_exp = expires_field(req)
if req_exp > 0 and now > req_exp then
  return {err = 'expired'}
end

local req_hash = hget(req, 'action_hash', '')
if req_hash == '' or req_hash ~= ARGV[1] then
  return {err = 'hash_mismatch'}
end

local req_id = hget(req, 'request_id', '')
local required_n = tonumber(hget(req, 'required_n', '0'))
local token_count = #KEYS - 1
if required_n > 0 and required_n ~= token_count then
  return {err = 'role_count_mismatch'}
end

-- Track roles and principals for SoD (distinct roles + distinct principals)
local seen_roles = {}
local seen_principals = {}

for i = 2, #KEYS do
  local tk = KEYS[i]
  if redis.call('EXISTS', tk) == 0 then
    return {err = 'missing_token'}
  end

  if hget(tk, 'used', '0') == '1' then
    return {err = 'token_used'}
  end

  local texp = expires_field(tk)
  if texp > 0 and now > texp then
    return {err = 'token_expired'}
  end

  if hget(tk, 'action_hash', '') ~= ARGV[1] then
    return {err = 'token_hash_mismatch'}
  end

  -- Case binding: token must belong to this request
  if req_id ~= '' then
    local tok_req = hget(tk, 'request_id', '')
    if tok_req ~= req_id then
      return {err = 'request_id_mismatch'}
    end
  end

  local role = hget(tk, 'role', '')
  if role == '' then
    return {err = 'missing_role'}
  end
  if seen_roles[role] then
    return {err = 'duplicate_role'}
  end
  seen_roles[role] = true

  local principal = hget(tk, 'principal', '')
  if principal == '' then
    return {err = 'missing_principal'}
  end
  if seen_principals[principal] then
    return {err = 'self_admit'}
  end
  seen_principals[principal] = true
end

-- All predicates passed — atomic burn
for i = 2, #KEYS do
  redis.call('HSET', KEYS[i], 'used', '1', 'used_at', ARGV[2])
end
redis.call('HSET', req, 'consumed', '1', 'consumed_at', ARGV[2])

return {ok = 'executed', n = tostring(token_count)}
