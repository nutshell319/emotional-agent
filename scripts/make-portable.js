/**
 * 构建 Warmth 便携版（单文件 .exe）
 *
 * 步骤：
 * 1. electron-builder 打包到 dist/win-unpacked
 * 2. 7za 压缩为 app.7z
 * 3. 拼接 7z SFX 模块 → Warmth-Portable.exe
 *
 * 用法：node scripts/make-portable.js
 * 输出：dist/Warmth-Portable.exe
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const UNPACKED = path.join(DIST, 'win-unpacked');
const SEVENZA = path.join(ROOT, 'node_modules', '7zip-bin', 'win', 'x64', '7za.exe');
const SFX_STUB = 'C:/Program Files/7-Zip/7z.sfx';

function run(cmd, opts = {}) {
  console.log(`  > ${cmd}`);
  return execSync(cmd, { cwd: ROOT, stdio: 'inherit', ...opts });
}

console.log('=== Step 1: electron-builder 打包 ===');
try {
  run('npx electron-builder --win dir', { timeout: 120000 });
} catch (e) {
  console.log('  (打包可能已存在或部分失败，继续...)');
}

if (!fs.existsSync(UNPACKED)) {
  console.error('  Error: dist/win-unpacked 不存在，打包失败');
  process.exit(1);
}

console.log('\n=== Step 2: 7z 压缩 ===');
const config = [
  ';!@Install@!UTF-8!',
  'Title="Warmth"',
  'BeginPrompt=""',
  'RunProgram="Warmth.exe"',
  ';!@InstallEnd@!',
].join('\n');

fs.writeFileSync(path.join(DIST, 'config.txt'), config);
run(`"${SEVENZA}" a -mx9 "${path.join(DIST, 'app.7z')}" "${UNPACKED}\\*"`, { timeout: 60000 });

console.log('\n=== Step 3: 拼接 SFX ===');
const sfx = fs.readFileSync(SFX_STUB);
const cfg = fs.readFileSync(path.join(DIST, 'config.txt'));
const archive = fs.readFileSync(path.join(DIST, 'app.7z'));
const output = path.join(DIST, 'Warmth-Portable.exe');

fs.writeFileSync(output, Buffer.concat([sfx, cfg, archive]));

// 清理临时文件
fs.unlinkSync(path.join(DIST, 'config.txt'));
fs.unlinkSync(path.join(DIST, 'app.7z'));

const sizeMB = (fs.statSync(output).size / 1024 / 1024).toFixed(1);
console.log(`\nDone: ${output} (${sizeMB} MB)`);
