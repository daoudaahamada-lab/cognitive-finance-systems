/** Funnel counts as returned by funnelFromStages (services/campaigns.ts). */
export type FunnelCounts = { invited: number; connected: number; messaged: number; replied: number; meetings: number };

export type FunnelRates = {
  /** Accepted invitations: connected / invited. */
  acceptance: number | null;
  /** Answers to the sequence: replied / messaged. */
  reply: number | null;
  /** Meetings per conversation: meetings / replied. */
  meeting: number | null;
};

const ratio = (part: number, whole: number) => (whole > 0 ? part / whole : null);

/** Conversion rates between funnel steps (0..1), null when the denominator is 0. Format with formatPercent. */
export function rates(funnel: FunnelCounts): FunnelRates {
  return {
    acceptance: ratio(funnel.connected, funnel.invited),
    reply: ratio(funnel.replied, funnel.messaged),
    meeting: ratio(funnel.meetings, funnel.replied),
  };
}
