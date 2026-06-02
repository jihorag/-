// 시각자료 템플릿 파라미터 검증.
// 의존성 없이 작은 자체 validator — Ajv 미사용 (번들 사이즈·복잡도 회피).
// 지원: 필수 키, 타입 체크, enum, array shape, nested object.
//
// Schema 예시:
//   { type:'object', required:['scenario','shifts'], properties:{
//       scenario: { type:'string' },
//       shifts: { type:'array', items:{
//         type:'object',
//         required:['curve','direction'],
//         properties:{
//           curve:{enum:['D','S']},
//           direction:{enum:['left','right']},
//           magnitude:{enum:['small','moderate','large'], default:'moderate'},
//           reason:{type:'string'},
//         }
//       }}
//   }}

function typeOf(v) {
  if (v === null) return 'null';
  if (Array.isArray(v)) return 'array';
  return typeof v;
}

function validateNode(schema, value, path = '$') {
  const errors = [];
  if (!schema) return errors;
  // null/undefined → required 처리는 부모에서
  if (value === undefined || value === null) {
    return errors;
  }
  const t = schema.type;
  const actualT = typeOf(value);
  if (t && actualT !== t) {
    errors.push(`${path}: expected ${t}, got ${actualT}`);
    return errors;
  }
  if (schema.enum && !schema.enum.includes(value)) {
    errors.push(`${path}: must be one of ${schema.enum.join('|')}, got ${JSON.stringify(value)}`);
  }
  if (t === 'object' && schema.properties) {
    const req = schema.required || [];
    for (const k of req) {
      if (value[k] === undefined || value[k] === null) {
        errors.push(`${path}.${k}: required`);
      }
    }
    for (const [k, subSchema] of Object.entries(schema.properties)) {
      if (value[k] !== undefined) {
        errors.push(...validateNode(subSchema, value[k], `${path}.${k}`));
      }
    }
  }
  if (t === 'array' && schema.items) {
    if (schema.minItems !== undefined && value.length < schema.minItems) {
      errors.push(`${path}: minItems ${schema.minItems}`);
    }
    value.forEach((item, i) => {
      errors.push(...validateNode(schema.items, item, `${path}[${i}]`));
    });
  }
  return errors;
}

// schema 기본값 자동 채우기 (coerce). 검증 전에 호출.
export function applyDefaults(schema, value) {
  if (!schema || value === undefined) return value;
  if (schema.type === 'object' && schema.properties && typeof value === 'object' && value !== null) {
    for (const [k, sub] of Object.entries(schema.properties)) {
      if (value[k] === undefined && sub.default !== undefined) {
        value[k] = sub.default;
      } else if (value[k] !== undefined) {
        applyDefaults(sub, value[k]);
      }
    }
  } else if (schema.type === 'array' && schema.items && Array.isArray(value)) {
    value.forEach((item) => applyDefaults(schema.items, item));
  }
  return value;
}

export function validate(schema, value) {
  applyDefaults(schema, value);
  const errors = validateNode(schema, value);
  return { ok: errors.length === 0, errors };
}
