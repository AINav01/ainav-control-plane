-- AINav Control Plane — dual (N-role) token consume
-- Atomic validate-all-then-write-all for multi-host admit.
--
-- KEYS[1]    = request HASH   e.g. ainav:req:{request_id}
-- KEYS[2..N] = token HASHes   e.g. ainav:tok:{request_id}:{token_id}
-- ARGV[1]    = expected action_hash (canonicalized in app; must match stored)
-- ARGV[2]    = now (unix seconds) for expiry checks
--
-- Request HASH fields:
--   request_id, action_hash, consumed, revoked, expires_at [, required_n]
-- Token HASH fields:
--   request_id, action_hash, role, principal, used, expires_at
--
-- Returns (stable machine contract):
--   Success: { ok = 'executed', n = '<token_count>' }
--   Business deny: { err = '<code>' }  optional { i = '<token_index>' } (1-based among tokens)
--   Programmer misuse: Redis error_reply (wrong numkeys)
--
-- Error handling rules:
--   1. Never write before every predicate passes (fail-closed).
--   2. Prefer return {err=} for dual denials — not error() — so clients can map codes.
--   3. Fail-fast order: ARGV → request existence → terminal request state → hash → count → tokens.
--   4. Flags consumed/revoked/used are true only when value == '1' (string).
--   5. No policy/OPA/canonical JSON/SoR I/O; no secrets in returns.
--
-- Docs: docs/REDIS_LUA_DUAL_ADMIT.md

local function fail(code, token_index)
  local r = { err = code }
  if token_index ~= nil then
    r.i = tostring(token_index)
  end
  return r
end

local function hget(key, field, default)
  local v = redis.call('HGET', key, field)
  if v == false or v == nil then
    return default
  end
  return v
end

local function is_flag_true(key, field)
  return hget(key, field, '0') == '1'
end

local function expires_at(key)
  -- Prefer expires_at (lab/product); accept expires for older seeds
  local v = redis.call('HGET', key, 'expires_at')
  if v == false then
    v = redis.call('HGET', key, 'expires')
  end
  if v == false or v == nil then
    return 0
  end
  local n = tonumber(v)
  if not n then
    return 0
  end
  return n
end

local function is_expired(key, now)
  local exp = expires_at(key)
  return exp > 0 and now > exp
end

--------------------------------------------------------------------------
-- 1) Invocation shape (programmer errors → error_reply)
--------------------------------------------------------------------------

if #KEYS < 2 then
  return redis.error_reply('numkeys must be >= 2 (request + at least one token)')
end

if type(ARGV[1]) ~= 'string' or ARGV[1] == '' then
  return fail('missing_expected_hash')
end

if ARGV[2] == false or ARGV[2] == nil or ARGV[2] == '' then
  return fail('missing_now')
end

local now = tonumber(ARGV[2])
if not now then
  return fail('invalid_now')
end

local expected_hash = ARGV[1]
local req = KEYS[1]
local token_count = #KEYS - 1

--------------------------------------------------------------------------
-- 2) Request: existence + terminal states (fast path under replay)
--------------------------------------------------------------------------

if redis.call('EXISTS', req) == 0 then
  return fail('unknown_request')
end

-- Replay / terminal states before expensive token loops
if is_flag_true(req, 'consumed') then
  return fail('already_consumed')
end

if is_flag_true(req, 'revoked') then
  return fail('revoked')
end

if is_expired(req, now) then
  return fail('expired')
end

--------------------------------------------------------------------------
-- 3) Request: write binding + case identity
--------------------------------------------------------------------------

local req_hash = hget(req, 'action_hash', '')
if req_hash == '' then
  return fail('missing_request_hash')
end
if req_hash ~= expected_hash then
  return fail('hash_mismatch')
end

local req_id = hget(req, 'request_id', '')
if req_id == '' then
  return fail('missing_request_id')
end

-- Optional: stored dual width must match KEYS token count
local required_n = tonumber(hget(req, 'required_n', '0')) or 0
if required_n > 0 and required_n ~= token_count then
  return fail('role_count_mismatch')
end

--------------------------------------------------------------------------
-- 4) Tokens: all predicates (no writes yet)
--------------------------------------------------------------------------

local seen_roles = {}
local seen_principals = {}

for i = 2, #KEYS do
  local tk = KEYS[i]
  local ti = i - 1 -- 1-based index among tokens (for client metrics; not PII)

  if redis.call('EXISTS', tk) == 0 then
    return fail('missing_token', ti)
  end

  if is_flag_true(tk, 'used') then
    return fail('token_used', ti)
  end

  if is_expired(tk, now) then
    return fail('token_expired', ti)
  end

  local tok_hash = hget(tk, 'action_hash', '')
  if tok_hash == '' then
    return fail('missing_token_hash', ti)
  end
  if tok_hash ~= expected_hash then
    return fail('token_hash_mismatch', ti)
  end

  -- Case binding: token must belong to this request
  local tok_req = hget(tk, 'request_id', '')
  if tok_req == '' then
    return fail('missing_token_request_id', ti)
  end
  if tok_req ~= req_id then
    return fail('request_id_mismatch', ti)
  end

  local role = hget(tk, 'role', '')
  if role == '' then
    return fail('missing_role', ti)
  end
  if seen_roles[role] then
    return fail('duplicate_role', ti)
  end
  seen_roles[role] = true

  local principal = hget(tk, 'principal', '')
  if principal == '' then
    return fail('missing_principal', ti)
  end
  if seen_principals[principal] then
    return fail('self_admit', ti)
  end
  seen_principals[principal] = true
end

--------------------------------------------------------------------------
-- 5) All predicates passed — atomic burn (single logical transition)
--------------------------------------------------------------------------

for i = 2, #KEYS do
  redis.call('HSET', KEYS[i], 'used', '1', 'used_at', ARGV[2])
end
redis.call('HSET', req, 'consumed', '1', 'consumed_at', ARGV[2])

return { ok = 'executed', n = tostring(token_count) }
