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

process.on('exit', () => {
  global.fetch = originalFetch;
});
