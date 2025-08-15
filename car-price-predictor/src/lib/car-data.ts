// Car data extracted from processed_car_data.csv
export const carBrands = [
  'alfa-romero',
  'audi',
  'bmw',
  'buick',
  'chevrolet',
  'dodge',
  'honda',
  'isuzu',
  'mazda',
  'maxda',
  'mercury',
  'mitsubishi',
  'nissan',
  'peugeot',
  'plymouth',
  'porsche',
  'renault',
  'saab',
  'subaru',
  'toyota',
  'toyouta',
  'volkswagen',
  'volvo',
  'vw'
] as const;

export const carTypesByBrand: Record<string, string[]> = {
  'alfa-romero': ['giulia', 'stelvio', 'Quadrifoglio'],
  'audi': ['100 ls', '100ls', 'fox', '5000s (diesel)'],
  'bmw': ['320i', 'x1', 'x3', 'z4'],
  'buick': ['electra 225 custom', 'century luxus (sw)', 'century'],
  'chevrolet': ['monte carlo', 'vega 2300'],
  'dodge': ['rampage', 'challenger se', 'd200', 'monaco (sw)', 'colt hardtop', 'colt (sw)', 'coronet custom', 'dart custom', 'coronet custom (sw)'],
  'honda': ['civic cvcc', 'civic', 'accord cvcc', 'accord lx', 'civic 1500 gl', 'accord', 'civic 1300', 'prelude', 'civic (auto)'],
  'isuzu': ['MU-X', 'D-Max ', 'D-Max V-Cross'],
  'mazda': ['rx3', 'glc deluxe', 'rx2 coupe', 'rx-4', '626', 'glc', 'rx-7 gs', 'glc 4', 'glc custom l', 'glc custom'],
  'maxda': ['rx3', 'glc deluxe'],
  'mercury': ['cougar'],
  'mitsubishi': ['mirage', 'lancer', 'outlander', 'g4', 'mirage g4', 'montero', 'pajero'],
  'nissan': ['versa', 'rogue', 'latio', 'titan', 'leaf', 'juke', 'note', 'clipper', 'nv200', 'dayz', 'fuga', 'otti', 'teana'],
  'peugeot': ['504', '304', '504 (sw)', '604sl', '505s turbo diesel'],
  'plymouth': ['fury iii', 'cricket', 'satellite custom (sw)', 'fury gran sedan', 'valiant', 'duster'],
  'porsche': ['macan'],
  'renault': ['12tl', '5 gtl'],
  'saab': ['99e', '99le', '99gle'],
  'subaru': ['unknown', 'dl', 'brz', 'baja', 'r1', 'r2', 'trezia', 'tribeca'],
  'toyota': ['corona mark ii', 'corona', 'corolla 1200', 'corona hardtop', 'corolla 1600 (sw)', 'carina', 'mark ii', 'starlet', 'tercel', 'cressida', 'celica gt', 'corolla liftback'],
  'toyouta': ['tercel'],
  'volkswagen': ['rabbit', '1131 deluxe sedan', 'model 111', 'type 3', '411 (sw)', 'super beetle', 'dasher', 'rabbit custom'],
  'volvo': ['145e (sw)', '144ea', '244dl', '245', '264gl', 'diesel'],
  'vw': ['dasher', 'rabbit', 'rabbit custom']
};

// Get car types for a specific brand
export function getCarTypesForBrand(brand: string): string[] {
  return carTypesByBrand[brand] || [];
}

// Get all unique car types
export function getAllCarTypes(): string[] {
  const allTypes = new Set<string>();
  Object.values(carTypesByBrand).forEach(types => {
    types.forEach(type => allTypes.add(type));
  });
  return Array.from(allTypes).sort();
}

// Get all unique brands (sorted)
export function getAllCarBrands(): string[] {
  return [...carBrands].sort();
}
