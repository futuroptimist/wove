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
