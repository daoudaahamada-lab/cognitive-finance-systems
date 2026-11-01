// Props of the "Short" composition: one short object of wth-videos/shorts/shorts.json, as is.
import type React from 'react';

export type ShortElement = {
  nom: string;
  role: string;
  geste?: string;
  couleur?: string;
};

export type DeviceName = 'folder' | 'beams' | 'line' | 'locks' | 'chat';

export type ShortProps = {
  id: string;
  titre: string;
  procede?: string;
  accroche: string;
  elements: ShortElement[];
  fin: string;
  legende?: string;
  hashtags?: string[];
  /** Visual device; absent = chosen from the id (S01 folder, S02 beams, S03 line, S04 locks, S05 chat). */
  device?: DeviceName;
};

export type RecapRow = {label: string; mark: 'tile' | 'check' | 'num'; color?: string};

export type DeviceSpec = {
  /** Everything between the progress bar and the role card, for the hook and the 5 elements (frame f, 0..END+10). */
  Stage: React.FC<{s: ShortProps; f: number}>;
  /** The device's final state, drawn centred on (0, 0) inside a ~190 x 250 box; k: 0 -> 1 entrance. */
  Emblem: React.FC<{s: ShortProps; k: number; u: number}>;
  /** Top of the role card (y px); null: the device shows the role itself (chat). */
  roleTop: number | null;
  /** Hook line (« accroche ») shown in the role card slot; false: the device shows it itself. */
  hookCard: boolean;
  recap: (s: ShortProps) => RecapRow[];
  /** The « fin » line is a risk warning (red warning sign). */
  finAlert?: boolean;
};
