export function normalizeAxisBounds(bounds) {
  if (!bounds || typeof bounds !== 'object') {
    return null;
  }
  const min = Number(bounds.min ?? bounds.min_mm ?? bounds.minimum ?? bounds.low);
  const max = Number(bounds.max ?? bounds.max_mm ?? bounds.maximum ?? bounds.high);
  if (!Number.isFinite(min) || !Number.isFinite(max) || max < min) {
    return null;
  }
  return { min, max };
}

export function comparePlannerToMachineBounds(plannerBounds, machineBounds) {
  const axes = [
    { key: 'x' },
    { key: 'y' },
    { key: 'z' },
    { key: 'e', plannerKeys: ['e', 'extrusion'], machineKeys: ['e', 'extrusion'] },
  ];
  const normalizedPlanner = {};
  const normalizedMachine = {};
  const missingPlannerAxes = [];
  const missingMachineAxes = [];

  const resolveAxisBounds = (source, keys, axisKey) => {
    if (!source || typeof source !== 'object') {
      return null;
    }
    const candidates = Array.isArray(keys) && keys.length > 0 ? keys : [axisKey];
    for (let index = 0; index < candidates.length; index += 1) {
      const candidate = normalizeAxisBounds(source?.[candidates[index]]);
      if (candidate) {
        return candidate;
      }
    }
    return null;
  };

  axes.forEach((axis) => {
    const { key, plannerKeys, machineKeys } = axis;
    normalizedPlanner[key] = resolveAxisBounds(plannerBounds, plannerKeys, key);
    normalizedMachine[key] = resolveAxisBounds(machineBounds, machineKeys, key);
    if (!normalizedPlanner[key]) {
      missingPlannerAxes.push(key);
    }
    if (!normalizedMachine[key]) {
      missingMachineAxes.push(key);
    }
  });

  const missingPlanner = missingPlannerAxes.length > 0;
  const missingMachine = missingMachineAxes.length > 0;
  const details = {};
  const exceedingAxes = [];

  axes.forEach(({ key }) => {
    const planner = normalizedPlanner[key];
    const machine = normalizedMachine[key];
    if (!planner || !machine) {
      return;
    }
    const overrunLow = planner.min < machine.min;
    const overrunHigh = planner.max > machine.max;
    if (overrunLow || overrunHigh) {
      exceedingAxes.push(key);
    }
    details[key] = {
      planner,
      machine,
      overrunLow,
      overrunHigh,
    };
  });

  const fits = !missingPlanner && !missingMachine && exceedingAxes.length === 0;

  return {
    missingPlanner,
    missingMachine,
    missingPlannerAxes,
    missingMachineAxes,
    fits,
    exceedingAxes,
    details,
  };
}

export function buildTravelEnvelopeBox(bounds, fallbackSpan) {
  if (!bounds) {
    return {
      width: fallbackSpan.x,
      depth: fallbackSpan.y,
      height: fallbackSpan.z,
      centerX: 0,
      centerY: 0,
      centerZ: 0,
    };
  }

  const width = Math.max((bounds.x?.max ?? 0) - (bounds.x?.min ?? 0), 0.0001);
  const depth = Math.max((bounds.y?.max ?? 0) - (bounds.y?.min ?? 0), 0.0001);
  const height = Math.max((bounds.z?.max ?? 0) - (bounds.z?.min ?? 0), 0.0001);

  const centerX = ((bounds.x?.max ?? 0) + (bounds.x?.min ?? 0)) / 2;
  const centerY = ((bounds.y?.max ?? 0) + (bounds.y?.min ?? 0)) / 2;
  const centerZ = ((bounds.z?.max ?? 0) + (bounds.z?.min ?? 0)) / 2;

  return {
    width: width < 0.001 ? fallbackSpan.x : width,
    depth: depth < 0.001 ? fallbackSpan.y : depth,
    height: height < 0.001 ? fallbackSpan.z : height,
    centerX: Number.isFinite(centerX) ? centerX : 0,
    centerY: Number.isFinite(centerY) ? centerY : 0,
    centerZ: Number.isFinite(centerZ) ? centerZ : 0,
  };
}
