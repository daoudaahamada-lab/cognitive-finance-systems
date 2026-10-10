import { describe, expect, it } from "vitest";
import { effectiveLimits, remainingQuota } from "@/server/domain/quotas";
import { isWithinSendingWindow } from "@/server/domain/schedule";
import { renderTemplate, unknownVariables, type TemplateVars } from "@/server/domain/templates";
import { parseFollowUps } from "@/server/domain/followups";

const vars: TemplateVars = {
  firstName: "Léa", lastName: "Martin", company: "Nova {Labs|Group}", title: "CFO", industry: "SaaS",
  location: "Paris", senderFirstName: "Alex", bookingUrl: "https://cal.example.com/x",
};

describe("templates", () => {
  it("fills variables and resolves spintax deterministically", () => {
    const tpl = "{Bonjour|Hello|Salut} {{firstName}}, {ravi|content} de vous lire.";
    const a = renderTemplate(tpl, vars, "p1");
    expect(a).toBe(renderTemplate(tpl, vars, "p1"));
    expect(a).toMatch(/^(Bonjour|Hello|Salut) Léa, (ravi|content) de vous lire\.$/);
  });

  it("never treats variable values as spintax", () => {
    expect(renderTemplate("Chez {{company}}", vars, "s")).toBe("Chez Nova {Labs|Group}");
  });

  it("supports nested spintax and variables inside options", () => {
    const out = renderTemplate("{Bonjour {{firstName}}|{Hello|Hi} {{firstName}}}", vars, "n");
    expect(["Bonjour Léa", "Hello Léa", "Hi Léa"]).toContain(out);
  });

  it("reports unknown variables", () => {
    expect(unknownVariables("Hi {{firstName}} {{prenom}}")).toEqual(["prenom"]);
  });
});

describe("quotas", () => {
  it("caps free accounts at 100 invites a week and 40 a day", () => {
    const limits = effectiveLimits({ accountType: "FREE", weeklyInviteLimit: null, dailyInviteLimit: null, dailyMessageLimit: null });
    expect(limits).toEqual({ weeklyInvites: 100, dailyInvites: 40, dailyMessages: 100 });
    expect(remainingQuota(limits, { invitesLast24h: 10, invitesLast7d: 95, messagesLast24h: 0 }).invites).toBe(5);
    expect(remainingQuota(limits, { invitesLast24h: 40, invitesLast7d: 40, messagesLast24h: 0 }).invites).toBe(0);
  });

  it("lets users lower limits but never raise them", () => {
    const limits = effectiveLimits({ accountType: "PREMIUM", weeklyInviteLimit: 500, dailyInviteLimit: 20, dailyMessageLimit: 1000 });
    expect(limits).toEqual({ weeklyInvites: 200, dailyInvites: 20, dailyMessages: 100 });
  });
});

describe("sending window", () => {
  const window = { timezone: "Europe/Paris", sendingDays: [1, 2, 3, 4, 5], sendingStart: "09:00", sendingEnd: "18:00" };

  it("respects local time and weekdays", () => {
    // Tuesday 2026-10-06 10:00 Paris = 08:00 UTC
    expect(isWithinSendingWindow(window, new Date("2026-10-06T08:00:00Z"))).toBe(true);
    // Tuesday 18:30 Paris
    expect(isWithinSendingWindow(window, new Date("2026-10-06T16:30:00Z"))).toBe(false);
    // Saturday 2026-10-10 11:00 Paris
    expect(isWithinSendingWindow(window, new Date("2026-10-10T09:00:00Z"))).toBe(false);
  });

  it("treats identical start and end as all day", () => {
    const allDay = { ...window, sendingDays: [6], sendingStart: "00:00", sendingEnd: "00:00" };
    expect(isWithinSendingWindow(allDay, new Date("2026-10-10T21:30:00Z"))).toBe(true); // Saturday 23:30 in Paris
    expect(isWithinSendingWindow(allDay, new Date("2026-10-09T09:00:00Z"))).toBe(false); // Friday
  });

  it("handles windows that wrap past midnight", () => {
    const night = { ...window, sendingDays: [1, 2, 3, 4, 5, 6, 7], sendingStart: "22:00", sendingEnd: "02:00" };
    expect(isWithinSendingWindow(night, new Date("2026-10-06T21:30:00Z"))).toBe(true); // 23:30 Paris
    expect(isWithinSendingWindow(night, new Date("2026-10-06T10:00:00Z"))).toBe(false);
  });
});

describe("follow-ups", () => {
  it("drops malformed JSON instead of crashing", () => {
    expect(parseFollowUps([{ delayDays: 3, template: "x" }])).toHaveLength(1);
    expect(parseFollowUps("nope")).toEqual([]);
    expect(parseFollowUps([{ delayDays: 0, template: "x" }])).toEqual([]);
  });
});
