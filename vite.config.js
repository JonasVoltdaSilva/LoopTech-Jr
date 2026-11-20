import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    watch: {
      // Test snapshots must not reload the app; OneDrive may lock license files.
      ignored: ['**/artifacts/**', '**/.venv/**', '**/public/licenses/**'],
    },
  },
});
