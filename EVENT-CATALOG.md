# DADE Event Catalog

**Discussion draft · 14 October 2026 · events describing the legal status of a person
and the authority others hold over their affairs**

This catalog summarizes all candidate DADE event types so they can be reviewed together.
DADE events describe **who may act for a person, and on what standing**, after that person
dies or loses capacity. They are drawn from a survey of 56 jurisdictions across 24
countries, where each underlying claim is cited to primary law with a retrieval date.

Events are organized into four groups. Each event reuses the shared DADE claims
(`governing_law`, `initiating_authority`, `canonical_role`, `evidence`,
`effect_unspecified`, `supersedes` / `corrects`) in addition to the key claims listed
below.

All event-type URIs use the base `https://schemas.openid.net/secevent/dade/event-type/`.

For each event's triggers, claims, the statute that requires them, Receiver responses, and
an example SET, see the [DADE Event Reference](dade-event-reference.html).

**Status legend** — **In spec**: defined in the [DADE 1.0 draft](openid-dade-events-1_0.md)
· **Candidate**: raised for discussion and not specified anywhere.

## The organizing principle: facts, not effects

A Transmitter asserting a DADE event asserts **that something happened**, not what follows
from it in law. This is a requirement, not reticence.

A court appoints a conservator over the property of someone who had granted a power of
attorney. Across seven US states that one transition has five different effects on the
existing power: in Virginia the agency continues; in West Virginia and Kentucky it
terminates; in Missouri the court allocates functions between the two fiduciaries; in
Nebraska and Kansas the conservator acquires the principal's own power to revoke it; and in
Iowa the power is *suspended* and later *reinstated* if the principal regains capacity.

An event asserting "the power of attorney is terminated" is therefore wrong in five of the
seven. One asserting "a conservator was appointed over this principal's property, under the
law of Iowa, as at this date" is right in all of them. Hence `governing_law` on every
event, and `effect_unspecified` for a Transmitter that will not characterise the
consequence.

## 1. The principal's state

*The two transitions in the person themselves. Both are reversible.*

| # | Event type | Status | Subject | What it signals | Key claims | Typical receiver action |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `principal-deceased` | **In spec** | Principal | A death has been recorded — by a registry, a clinician, a court, or a report with none of those behind it | `record_status` `date_of_death` `death_type` `proof` `registry_reference` | Grant nothing; stop inactivity clocks; freeze destructive automation; prepare to evaluate a claim |
| 2 | `principal-capacity-changed` | **In spec** | Principal | A determination about capacity has been made, or has ceased to hold | `capacity_status` `determiner` `scope` `finding_date` `expires_at` `objection` | Suspend or revive exactly what the governing law attaches to the finding |

Both carry a correction path, and for the same reason: a death record can be withdrawn, and
a capacity finding can be reversed on re-examination or expire by statute. The surveyed
shelf lives on a capacity determination run from two hours to five years.

## 2. Authority lifecycle

*The standing of someone acting for the principal.*

| # | Event type | Status | Subject | What it signals | Key claims | Typical receiver action |
| --- | --- | --- | --- | --- | --- | --- |
| 3 | `authority-changed` | **In spec** | Principal (holder in body) | An authority was granted, registered, suspended, reinstated, re-scoped, devolved or terminated | `authority_status` `holder` `artefact` `scope` `registration_effect` `revival` `cause` `predecessor` | Evaluate against `governing_law`; act on the conclusion, not the status name |
| 4 | `authority-lapse-pending` | Candidate | Principal | An authority is about to end by the running of time, with nobody required to say so | `lapses_at` `cause` `grace_period` `preventable_by` | Tell the holder, and the alternate where the authority devolves rather than ends |

Three `authority_status` values exist because the surveyed law requires them and a
two-state model cannot express them:

- **`suspended` / `reinstated`** — an authority may be valid, temporarily ineffective, and
  effective again, with nothing issued or withdrawn at either boundary.
- **`registered`** — in ten of the forty-four jurisdictions that record the point, a power must
  be registered before
  it can be used, so the instrument can exist, be valid, and confer nothing. In one of them
  registration is *constitutive*: the power is not created unless registered.
  `registration_effect` carries the difference.

And `artefact` has the value **`none`**, which is not an error: in 16 of the 24 countries
surveyed the heirs hold the estate from the moment of death, with no document issued and
nobody declaring anything. Paired with `initiating_authority: operation-of-law`, that is
the honest description of the most common succession regime there is.

> **On `authority-lapse-pending`:** the open question is whether this is an event at all or
> a field on `authority-changed`. Against: a pending lapse is not a transition, and a
> Transmitter that knows `lapses_at` could have put it on the `granted` event. For: in the
> disposition-of-remains case the clock starts on a *notification* the granting Transmitter
> has no knowledge of — twenty-four hours from the holder being told of the death, or forty
> hours from the death, whichever is earlier.

## 3. The principal's own directions

*What the principal told a custodian, which is not the same as who they appointed.*

| # | Event type | Status | Subject | What it signals | Key claims | Typical receiver action |
| --- | --- | --- | --- | --- | --- | --- |
| 5 | `direction-recorded` | **In spec** | Principal | The principal lodged a direction about post-mortem access, or withdrew one | `direction_status` `effect` `lodged_with` `designee` `scope` `precedence` `revocable` | Record it and honour it; a `forbid` needs no corroborating authority |

The `effect` claim takes **`permit` or `forbid`**, and the prohibiting case is the reason
this is not a variant of `authority-changed`. In one surveyed jurisdiction a deceased
person's data-protection rights are exercisable by an interested person *unless the deceased
forbade it in writing to the controller* — and that prohibition binds. An implementation
built for the permitting case silently mis-implements the prohibiting one.

`precedence` is a bargain rather than a boast: the statutes that let an in-product direction
override a contrary direction in a will do so **on condition** that the tool permits the
user to modify or delete it at any time, which is why `revocable` sits beside it.

## 4. Presentation, acceptance and refusal

*The exchange at the counter. These are the events a custodian sends.*

| # | Event type | Status | Subject | What it signals | Key claims | Typical receiver action |
| --- | --- | --- | --- | --- | --- | --- |
| 6 | `authority-presented` | Candidate | Principal | A holder presented an authority; statutory response clocks start here | `holder` `artefact` `asks` `presented_at` `response_deadline` | Acknowledge, start the clock, answer within it |
| 7 | `authority-accepted` | Candidate | Principal | A custodian accepted an authority and will act on it | `holder` `artefact` `scope_honoured` `effective_at` `conditions` | Open what was accepted and no more |
| 8 | `authority-refused` | **In spec** | Principal | A custodian declined to honour an authority, and states the ground | `grounds` `holder` `presented_at` `artefact` `report_deadline` `remediable` | Where the Receiver is the issuing authority, treat it as the governing law makes it |

`authority-refused` **travels in the opposite direction to every other event in this
profile**, and it exists because at least one legislature already requires it: a person
refusing to accept the authority of a guardian or conservator must, within ten days of the
refusal, report the refusal and its reason to the court that issued the letters of office,
where it is treated as a grievance. A deployment supporting it needs a stream in which the
issuing authority is the Receiver.

Its `grounds` registry is drawn from statutes that enumerate the grounds on which an
authority may lawfully be refused. Two grounds are expressly **prohibited** and must never
be sent: a refusal resting exclusively on the age or date of execution of the instrument,
and one resting exclusively on a requirement that a different form of instrument be used.

> **Privacy note on `authority-presented`:** it is the one event that carries data
> identifying a living claimant, and the one least suited to a broadcast stream. It may
> belong in a bilateral exchange between the holder's service and the custodian rather than
> in a Shared Signals stream at all.

## What the catalog does not cover

- **The content of an authority.** What an executor may do with an account is a matter for
  the custodian's terms and the law of the estate, not for an event.
- **Identity proofing of the claimant.** Where evidence travels with an event it uses the
  `evidence` structures of OpenID Connect for Identity Assurance; this profile defines no
  new ones.
- **Authorization.** A Receiver's decision to grant or deny access is local policy. Nothing
  in the catalog is a command.
- **The legal consequence of any transition.** See the organizing principle above.
