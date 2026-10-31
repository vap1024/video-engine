#!/usr/bin/env node
/**
 * video-engine - render inserts through the Remotion Node API.
 * Run it via engine/render-remotion.sh (fresh network namespace):
 * on some hosts Remotion cannot pick a port because connect probes
 * to 0.0.0.0 / :: are intercepted, and some system Chromium builds
 * block http://localhost outright. Use Remotion's own Chrome
 * Headless Shell (installed by `npx remotion browser ensure`).
 *
 * Usage:
 *   node render.mjs still <CompId> <out.png> '<propsJson>'
 *   node render.mjs video <CompId> <out.mp4>
 */
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {selectComposition, renderStill, renderMedia} from '@remotion/renderer';

const CHROME = path.resolve(
  'node_modules/.remotion/chrome-headless-shell/linux64/chrome-headless-shell-linux64/chrome-headless-shell'
);
// Remotion 4.0.x: chromiumOptions has no `args` field - custom Chrome
// flags cannot be passed through it.
const chromiumOptions = {enableMultiProcessOnLinux: true};

const [, , mode, compId, out, propsJson] = process.argv;
const entry = path.resolve('src/index.ts');

const serveUrl = await bundle({entryPoint: entry, webpackOverride: (c) => c});
const inputProps = propsJson ? JSON.parse(propsJson) : {};
const composition = await selectComposition({
  serveUrl,
  id: compId,
  inputProps,
  browserExecutable: CHROME,
  chromiumOptions,
});

if (mode === 'still') {
  await renderStill({
    composition,
    serveUrl,
    output: path.resolve(out),
    inputProps,
    browserExecutable: CHROME,
    chromiumOptions,
    imageFormat: 'png',
  });
  console.log('STILL OK', out);
} else if (mode === 'video') {
  await renderMedia({
    composition,
    serveUrl,
    codec: 'h264',
    crf: 18,
    outputLocation: path.resolve(out),
    inputProps,
    browserExecutable: CHROME,
    chromiumOptions,
    concurrency: 2,
    enforceAudioTrack: false,
  });
  console.log('VIDEO OK', out);
} else {
  throw new Error('mode must be still|video');
}
