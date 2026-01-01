export function setTone(element, tone) {
  if (!element) {
    return;
  }

  if (tone) {
    element.dataset.tone = tone;
  } else if (element.dataset && element.dataset.tone) {
    delete element.dataset.tone;
  }
}
