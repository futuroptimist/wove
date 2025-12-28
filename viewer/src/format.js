export function formatFileSize(bytes) {
  const numeric = Number(bytes);
  if (!Number.isFinite(numeric) || numeric < 0) {
    return null;
  }
  if (numeric === 0) {
    return '0 B';
  }
  if (numeric < 1024) {
    return `${Math.round(numeric)} B`;
  }
  if (numeric >= 1024 * 1024) {
    return `${(numeric / (1024 * 1024)).toFixed(2)} MB`;
  }
  const kilobytes = numeric / 1024;
  const roundedKilobytes = Math.round(kilobytes * 10) / 10;
  return `${roundedKilobytes.toFixed(1)} kB`;
}
