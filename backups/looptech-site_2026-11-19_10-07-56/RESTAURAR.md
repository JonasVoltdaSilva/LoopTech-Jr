# Verified backup - 2026-11-19_10-07-56

Complete project copy (2150 files): code, assets, configuration, dist, artifacts, node_modules and .venv. All SHA-256 hashes checked against source in manifest.sha256.json. Project instructions and memory snapshot are in context/.

## Safe restore (PowerShell)

Stop any server using the destination. Copy to a NEW directory, without deleting or overwriting existing work:

```powershell
Copy-Item -LiteralPath "C:\Users\Jhonny\OneDrive\Área de Trabalho\SKILLS PARA O CODEX\backups\looptech-site_2026-11-19_10-07-56\project" -Destination "C:\Users\Jhonny\OneDrive\Área de Trabalho\SKILLS PARA O CODEX\looptech-site-restaurado_2026-11-19_10-07-56" -Recurse
```

Then run `npm.cmd run dev -- --port 5182 --strictPort` inside the restored directory and open http://127.0.0.1:5182/. To restore the original path instead, preserve its current directory under another name before copying project back.
