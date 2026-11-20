import { defineConfig } from 'vite';

export default defineConfig({
  base: process.env.GITHUB_ACTIONS === 'true' ? '/LoopTech-Jr/' : '/',
  server: {
    watch: {
      // Test snapshots must not reload the app; OneDrive may lock license files.
      ignored: ['**/artifacts/**', '**/.venv/**', '**/public/licenses/**'],
    },
  },
});
