type PlanetaireFontSource = {
  url: string;
  format?: string;
};

type PlanetaireFontFace = {
  family?: string;
  sources: PlanetaireFontSource[];
  style?: string;
  weight?: number | string;
};

type PlanetaireFontLicense = {
  availability?: string;
  name?: string;
  notes?: string;
  shortName?: string | null;
  spdx?: string | null;
  url?: string | null;
};

type PlanetaireFontMetrics = {
  advance: number;
  cap: number;
  xHeight: number;
};

type PlanetaireFont = {
  availability?: string;
  default?: boolean;
  description: string;
  faces?: PlanetaireFontFace[];
  family: string;
  id: string;
  license?: PlanetaireFontLicense;
  metrics?: PlanetaireFontMetrics | null;
  name: string;
  npmDownloadsLastMonth?: number;
  source: string;
};

interface Window {
  PlanetaireFontData?: {
    brandUsage?: unknown[];
    fonts: PlanetaireFont[];
    nerdFontsEcosystem?: unknown;
    npmDownloadWindow?: unknown;
    trackedFonts?: unknown[];
    updated?: string;
  };
  applyCompareThemeVars?: (theme: string) => void;
}
