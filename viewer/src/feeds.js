export function computeYarnFeedIndices(events, baselineExtrusion = null) {
  if (!Array.isArray(events) || events.length === 0) {
    return [];
  }

  const feedIndices = new Set();
  const feedCommentPattern = /feed/i;
  const feedDeltaTolerance = 0.01;

  let previousExtrusion = Number.isFinite(baselineExtrusion) ? baselineExtrusion : null;

  events.forEach((event, index) => {
    if (!event || typeof event !== 'object') {
      return;
    }

    const comment = typeof event.comment === 'string' ? event.comment : '';
    if (comment && feedCommentPattern.test(comment)) {
      feedIndices.add(index);
    }

    const extrusionValue = Number(event.extrusion);
    const extrusion = Number.isFinite(extrusionValue) ? extrusionValue : null;
    if (extrusion === null) {
      return;
    }

    if (previousExtrusion !== null) {
      const delta = extrusion - previousExtrusion;
      if (Number.isFinite(delta) && delta > feedDeltaTolerance) {
        feedIndices.add(index);
      }
    }

    previousExtrusion = extrusion;
  });

  return Array.from(feedIndices.values());
}
