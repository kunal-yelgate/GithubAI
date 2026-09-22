import test from 'node:test';
import assert from 'node:assert/strict';

const originalFetch = global.fetch;

const { askAI } = await import('./api.js');

test('askAI surfaces backend error details when the error body is not JSON', async () => {
  global.fetch = async () => ({
    ok: false,
    json: async () => {
      throw new Error('Unexpected end of JSON input');
    },
  });

  await assert.rejects(
    askAI('hello'),
    { message: 'AI request failed' }
  );

  global.fetch = originalFetch;
});

test('askAI returns a helpful error when the backend is unreachable', async () => {
  global.fetch = async () => {
    throw new TypeError('Failed to fetch');
  };

  await assert.rejects(
    askAI('hello'),
    { message: /backend|configured|running/i }
  );

  global.fetch = originalFetch;
});

test('askAI turns a 401 into a login prompt instead of a network error', async () => {
  global.fetch = async () => ({
    ok: false,
    status: 401,
    json: async () => ({ detail: 'Not authenticated' }),
  });

  await assert.rejects(
    askAI('hello'),
    { message: /log in again|session has expired/i }
  );

  global.fetch = originalFetch;
});

process.on('exit', () => {
  global.fetch = originalFetch;
});
