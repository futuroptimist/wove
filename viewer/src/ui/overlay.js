export function updateRoadmapPanel(dom, title, description) {
  if (!dom || !dom.roadmapTitleElement || !dom.roadmapDescriptionElement) {
    return;
  }

  dom.roadmapTitleElement.textContent = title ?? '';
  dom.roadmapDescriptionElement.textContent = description ?? '';
}
