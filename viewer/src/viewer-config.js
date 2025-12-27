export const patternPreviewSource = 'assets/base_chain_row.planner.json';
export const defaultPatternPreviewDurationSeconds = 14;
export const plannerUploadLimitBytes = 10 * 1024 * 1024;

export const fallbackPatternPlannerEvents = [
  { comment: 'use millimeters', x: 0.0, y: 0.0, z: 4.0, extrusion: 0.0 },
  { comment: 'absolute positioning', x: 0.0, y: 0.0, z: 4.0, extrusion: 0.0 },
  { comment: 'zero axes', x: 0.0, y: 0.0, z: 4.0, extrusion: 0.0 },
  { comment: 'chain stitch 1 of 3: plunge', x: 0.0, y: 0.0, z: -1.5, extrusion: 0.0 },
  { comment: 'chain stitch 1 of 3: feed yarn', x: 0.0, y: 0.0, z: -1.5, extrusion: 0.5 },
  { comment: 'chain stitch 1 of 3: raise', x: 0.0, y: 0.0, z: 4.0, extrusion: 0.5 },
  { comment: 'chain stitch 1 of 3: advance', x: 5.0, y: 0.0, z: 4.0, extrusion: 0.5 },
  { comment: 'chain stitch 2 of 3: plunge', x: 5.0, y: 0.0, z: -1.5, extrusion: 0.5 },
  { comment: 'chain stitch 2 of 3: feed yarn', x: 5.0, y: 0.0, z: -1.5, extrusion: 1.0 },
  { comment: 'chain stitch 2 of 3: raise', x: 5.0, y: 0.0, z: 4.0, extrusion: 1.0 },
  { comment: 'chain stitch 2 of 3: advance', x: 10.0, y: 0.0, z: 4.0, extrusion: 1.0 },
  { comment: 'chain stitch 3 of 3: plunge', x: 10.0, y: 0.0, z: -1.5, extrusion: 1.0 },
  { comment: 'chain stitch 3 of 3: feed yarn', x: 10.0, y: 0.0, z: -1.5, extrusion: 1.5 },
  { comment: 'chain stitch 3 of 3: raise', x: 10.0, y: 0.0, z: 4.0, extrusion: 1.5 },
  { comment: 'chain stitch 3 of 3: advance', x: 15.0, y: 0.0, z: 4.0, extrusion: 1.5 },
  { comment: 'pause for 0.400 s', x: 15.0, y: 0.0, z: 4.0, extrusion: 1.5 },
  { comment: 'reposition', x: 18.0, y: 5.0, z: 4.0, extrusion: 1.5 },
  { comment: 'turn to next row', x: 0.0, y: 12.0, z: 4.0, extrusion: 1.5 },
  { comment: 'single stitch 1 of 1: plunge', x: 0.0, y: 12.0, z: -2.0, extrusion: 1.5 },
  { comment: 'single stitch 1 of 1: feed yarn', x: 0.0, y: 12.0, z: -2.0, extrusion: 2.1 },
  { comment: 'single stitch 1 of 1: raise', x: 0.0, y: 12.0, z: 4.0, extrusion: 2.1 },
  { comment: 'single stitch 1 of 1: advance', x: 4.5, y: 12.0, z: 4.0, extrusion: 2.1 },
];
Object.freeze(fallbackPatternPlannerEvents);

export const fallbackPatternDefaults = {
  safe_z_mm: 4.0,
  fabric_plane_z_mm: 0.0,
  travel_feed_rate_mm_min: 1200,
  plunge_feed_rate_mm_min: 600,
  yarn_feed_rate_mm_min: 300,
  default_row_height_mm: 6.0,
  row_spacing_mm: 6.0,
  require_home: false,
  home_state: 'unknown',
};
Object.freeze(fallbackPatternDefaults);

export const spoolPrePulseSettings = {
  speed: 2.8,
  phaseOffset: Math.PI / 10,
};

export const spoolProgressTonePalette = {
  neutral: { color: 0xffb173, emissive: 0xff8c2f },
  info: { color: 0x9ee5ff, emissive: 0x48c2ff },
  ready: { color: 0x9fffd7, emissive: 0x36e2ad },
  warning: { color: 0xffc27d, emissive: 0xff8c2f },
};

export const fallbackMessages = {
  machineProfileFallbackMessage:
    'Machine profile metadata unavailable. Export with --machine-profile to surface axis settings.',
  machineProfileEnvelopeFallbackMessage:
    'Machine profile envelope unavailable. Include travel_min_mm and '
    + 'travel_max_mm for each axis.',
  machineProfileEnvelopeMissingAxesPrefix:
    'Machine profile envelope unavailable — add travel_min_mm and travel_max_mm for: ',
  boundsComparisonFallbackMessage:
    'Bounds comparison unavailable. Export planner bounds and '
    + 'machine profile limits to compare.',
  homingGuardFallbackMessage:
    'Homing guard metadata unavailable. Export planner defaults.require_home and '
    + 'defaults.home_state.',
  homingGuardPositionFallbackMessage: 'Coordinates: Awaiting planner coordinates…',
  heatedBedStatusFallbackMessage:
    'Thermistor conduit reserved for the heater upgrade — planner status drives the glow '
    + 'along the wiring path.',
  heatedBedMetadataMissingMessage:
    'Heated bed conduit metadata missing — include heated_bed_conduit defaults to drive the glow.',
  heatedBedRouteFallbackMessage:
    'Conduit status: Illuminating the bay-to-bed run so heater wiring stays obvious during '
    + 'dry runs.',
  patternBoundsFallbackMessage:
    'Planner bounds unavailable. Export --format planner payloads with bounds to preview '
    + 'the motion envelope.',
  patternDefaultsFallbackMessage:
    'Planner defaults unavailable. Export planner payloads with defaults metadata to '
    + 'surface feed and height settings.',
  plannerMetadataFallbackMessage:
    'Planner metadata unavailable. Export planner payloads with version and units fields '
    + 'to surface schema details.',
  yarnFlowStatusFallbackMessage:
    'Yarn flow monitor idle — load a planner preview to track feed events.',
  yarnFlowSpoolFallbackMessage: 'Spool status: Parked until planner preview loads.',
  yarnFlowTotalFallbackMessage: 'Total yarn fed: Awaiting planner preview…',
  yarnFlowProgressFallbackMessage: 'Spool progress: Awaiting planner preview…',
  yarnFlowRateFallbackMessage: 'Feed rate: Awaiting yarn feed telemetry…',
  yarnFlowQueueFallbackMessage: 'Remaining feed pulses: Awaiting planner preview…',
  yarnFlowUpcomingFallbackMessage: 'Next feed pulses: Awaiting planner preview…',
  yarnFlowTimingFallbackMessage: 'Feed timing: Awaiting planner preview…',
  yarnFlowCycleFallbackMessage: 'Cycle pacing: Awaiting planner preview…',
  yarnFlowCalibrationFallbackMessage:
    'Calibration: Awaiting tension sensor calibration metadata.',
  yarnFlowTensionFallbackMessage: 'Tension telemetry: Awaiting planner preview…',
  yarnFlowPositionFallbackMessage: 'Coordinates: Awaiting yarn flow coordinates…',
  spoolProgressCountdownFallbackMessage: 'Next feeds: Awaiting Yarn Flow timing…',
  spoolCountdownPausedMessage:
    'Countdown ribbon pinned while the preview is paused — resume to advance timing.',
};
