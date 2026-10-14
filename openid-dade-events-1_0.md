---
stand_alone: true
ipr: none
cat: info
submissiontype: IETF
wg: OpenID Shared Signals

docname: openid-dade-events-1_0

title: "OpenID Death and the Digital Estate Event Profile 1.0 - draft 00"
abbrev: DADE-Events
lang: en
kw:
 - security events
 - shared signals
 - digital estate
 - delegated authority
 - death
 - incapacity
 - SET

author:
- ins: M. Kiser
  name: Mike Kiser
  org: SailPoint

normative:
  RFC2119:
  RFC5646:
  RFC8174:
  RFC8417:
  RFC8935:
  RFC8936:
  RFC9493:
  SSF:
    title: "OpenID Shared Signals Framework Specification 1.0"
    target: https://openid.net/specs/openid-sharedsignals-framework-1_0.html
    date: 2025
  IDA:
    title: "OpenID Connect for Identity Assurance 1.0"
    target: https://openid.net/specs/openid-connect-4-identity-assurance-1_0-final.html
    date: 2024

informative:
  DADE-PAPER:
    title: "The Unfinished Digital Estate: Culture, Law, and Technology after Death"
    target: https://openid.net/wp-content/uploads/2026/03/The-Unfinished-Digital-Estate-Final.pdf
    author:
      - ins: H. Flanagan
        name: Heather Flanagan
      - ins: M. Kiser
        name: Mike Kiser
      - ins: D. Saxe
        name: Dean H. Saxe
    date: 2026
  DADE-EVENTS:
    title: "DADE Event Reference"
    target: https://derrumbe.github.io/openid-dade-events/dade-event-reference.html
    date: 2026
  ROLES:
    title: "Digital Estate Roles: when authority is assigned, when it starts, and when it ends"
    target: https://xebecstudios.org/research/digital-estate-roles/
    date: 2026

--- abstract

This document defines a set of Security Event Tokens (SETs) {{RFC8417}} for
transmission over the OpenID Shared Signals Framework {{SSF}} describing the
legal transitions that govern access to a person's accounts when that person
dies or loses capacity: the recording of a death, a finding of incapacity or its
reversal, the grant, registration, suspension, reinstatement, termination and
devolution of a legal authority over the person or their estate, a direction the
person lodged with a custodian, and a custodian's refusal to honour an authority
presented to it.

The events in this profile carry facts, not their legal consequences. The same
transition has materially different effects in different jurisdictions, so a
Receiver evaluating what an event means does so against the law of the
principal's domicile as at a stated date, and this profile provides the fields
required to do that rather than asserting a result.

--- middle

# Introduction

When a person dies or loses the capacity to act, legal authority over their
affairs — and so over their accounts — passes to someone else. Who that is, when
the authority starts, what bounds it, and when it ends are questions of law, and
the answers vary widely between jurisdictions. A survey of 57 jurisdictions
across 24 countries {{ROLES}} finds that almost nothing in this area is a query:
nearly every question a custodian faces is the consequence of a **state
transition**. Someone died. A clinician recorded a finding. A court appointed a
fiduciary. Capacity returned. A clock expired.

That shape is the shape the Shared Signals Framework {{SSF}} already serves. What
has been missing is a vocabulary for these particular transitions.

The gap is recorded in {{DADE-PAPER}}, which observes that no widely adopted
framework ties identity delegation to estate events, and that the field lacks
standardized mechanisms to express delegated access rights together with the
state changes of the data owner — incapacitation notices, digital death
certificates, the assignment of an executor. This document proposes the event
vocabulary for those state changes.

## Relationship to Other Event Sets

The Shared Signals Framework specifies the transport: stream configuration and
management, and delivery by push {{RFC8935}} or poll {{RFC8936}} of SETs about
subjects identified per {{RFC9493}}. The event sets carried over it are separate
documents, each scoped to a subject matter. This profile is one such set. Its
subject matter — the legal status of a person and the authority others hold over
their affairs — is not addressed by any existing set, and this document neither
extends nor profiles any of them.

An implementation that already operates an SSF transmitter or receiver reuses it
unchanged. What it gains here is the event types in {{event-types}}, the common
claims in {{common-event-claims}}, and the subject format in
{{principal-subject}}.

## Scope

In scope: the transitions that change who may act for a person, or that change
the standing of someone already acting.

Out of scope, and deliberately so:

- **The legal consequence of a transition.** See {{facts-not-effects}}.
- **The content of any authority.** What an executor may do with an account is a
  matter for the custodian's terms and the law of the estate, not for an event.
- **Identity proofing of the claimant.** Where evidence travels with an event it
  uses the structures of {{IDA}}; this profile does not define new ones.
- **Authorization.** A Receiver's decision to grant or deny access on the
  strength of an event is local policy. Nothing in this profile is a command.

## Facts, not Effects {#facts-not-effects}

A Transmitter asserting one of these events asserts **that something happened**,
not what follows from it in law. This is not reticence; it is a requirement
drawn from the jurisdictional survey.

Consider a single transition: a court appoints a conservator over the property
of a person who had previously granted a power of attorney. Across seven US
states that one event has five different effects on the existing power: in
Virginia the agency continues; in West Virginia and Kentucky it terminates; in
Missouri the court allocates functions between the two fiduciaries; in Nebraska
and Kansas the conservator acquires the principal's own power to revoke it; and
in Iowa the power is **suspended** and later **reinstated** if the principal
regains capacity.

An event that asserted "the power of attorney is terminated" would therefore be
wrong in five of those seven states. An event asserting "a conservator was
appointed over this principal's property, under the law of Iowa, as at this
date" is correct in all of them, and leaves the consequence to be evaluated by
whoever is entitled to evaluate it.

Accordingly every event in this profile carries `governing_law`
({{common-event-claims}}), and a Transmitter that cannot or will not characterise
the legal effect of the transition it is reporting SHOULD set
`effect_unspecified` to `true`.

## Notational Conventions

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in BCP 14 {{RFC2119}} {{RFC8174}}
when, and only when, they appear in all capitals, as shown here.

The terms Transmitter, Receiver, Stream, Subject and SET are used as defined in
{{SSF}} and {{RFC8417}}.

**Principal** denotes the person whose death, capacity or affairs the event
concerns. **Holder** denotes a party who holds, claims, or is refused an
authority over the Principal or their estate.

# Common Event Claims {#common-event-claims}

The following claims MAY appear in any event defined by this profile unless an
event definition specifies otherwise.

Attributes:

- **event_timestamp** - OPTIONAL, JSON number: the time at which the transition
  described by this SET took effect in law, as distinct from the time it was
  recorded or detected. Its value is the number of seconds from
  1970-01-01T0:0:0Z as measured in UTC. Where the two differ — a death
  registered three days after it occurred — the Transmitter SHOULD use the legal
  time and MAY convey the recording time in `reason_admin`.
- **initiating_authority** - RECOMMENDED, JSON string: who declared the
  transition. The weight a Receiver gives an event depends substantially on this
  value. It MUST be one of the following, or any other value mutually understood
  by the Transmitter and Receiver:
    - `court` - a court or tribunal.
    - `registrar` - a civil registry or register of deaths, births or titles.
    - `notary` - a notary or equivalent public officer.
    - `clinician` - a physician, psychologist, nurse practitioner or other
      health professional authorised to make the relevant determination.
    - `agency` - a government department or agency acting administratively.
    - `principal` - the Principal themselves, for example in revoking an
      authority they granted.
    - `custodian` - the party holding the asset, for example in refusing an
      authority presented to it.
    - `claimant` - the Holder or putative Holder, for example in presenting an
      authority.
    - `operation-of-law` - **nobody declared it.** The transition took effect by
      operation of law without any instrument or declaration. This value is not
      a formality: in 16 of the 24 countries surveyed in {{ROLES}} the heirs hold
      the estate from the moment of death with no document issued and no
      authority declaring anything, and an event set unable to say so cannot
      describe a third of the world.
- **governing_law** - RECOMMENDED, JSON object: the law against which the
  consequence of this event is to be evaluated. It MUST contain:
    - `jurisdiction` - REQUIRED, JSON string: the jurisdiction whose law
      governs. Implementations SHOULD use a subdivision code per ISO 3166-2
      where the governing law is sub-national (`US-IA`, `CA-QC`, `AU-VIC`) and
      ISO 3166-1 alpha-2 otherwise (`FR`, `SG`).
    - `as_at` - REQUIRED, JSON string: the date, in the format YYYY-MM-DD, as at
      which that jurisdiction's law is to be read.
  The `as_at` value is not redundant with `event_timestamp`. A jurisdiction may
  amend a provision with retroactive effect, so the law as at a past date is not
  fixed merely because the date has passed; {{ROLES}} records an amendment of
  this kind taking effect retroactively to a date nine months earlier.
- **canonical_role** - OPTIONAL, JSON string: the role the Holder holds or
  claims, drawn from a cross-jurisdiction role vocabulary so that an executor, a
  liquidator and a *Nachlassverwalter* can be recognised as the same role. The
  vocabulary of {{ROLES}} is RECOMMENDED; values include
  `personal-representative-executor`, `conservator-estate`,
  `financial-poa-durable`, `small-estate-affiant`, `successor-trustee`,
  `online-tool-designee` and `disposition-of-remains-agent`.
- **evidence** - OPTIONAL, JSON array: evidence supporting the assertion,
  expressed using the `evidence` structures of {{IDA}}. Its `document`,
  `electronic_record` and `vouch` types already cover, respectively, a death
  certificate, a register entry, and a third party attesting to someone's
  standing, and this profile does not define alternatives.
- **effect_unspecified** - OPTIONAL, JSON boolean: when `true`, the Transmitter
  asserts the fact of the transition and expressly does not characterise its
  legal consequence. See {{facts-not-effects}}. A Receiver MUST NOT infer a
  consequence the Transmitter has declined to assert.
- **supersedes** - OPTIONAL, JSON string: the `jti` of an earlier SET from the
  same Transmitter that this event replaces.
- **corrects** - OPTIONAL, JSON string: the `jti` of an earlier SET from the same
  Transmitter that this event corrects or withdraws. A Receiver that has acted on
  the corrected event SHOULD unwind that action so far as it is able, and the
  Transmitter SHOULD describe the correction in `reason_admin`.
- **reason_admin** - OPTIONAL, JSON object: a localizable administrative message
  intended for logging and auditing. The object MUST contain one or more
  key/value pairs, with a BCP 47 {{RFC5646}} language tag as the key and the
  locale-specific message as the value.
- **reason_user** - OPTIONAL, JSON object: a localizable end-user-friendly
  message, structured identically to `reason_admin`.

The following example is non-normative.

~~~ json
{
  "initiating_authority": "court",
  "governing_law": { "jurisdiction": "US-IA", "as_at": "2026-10-14" },
  "effect_unspecified": true,
  "reason_admin": {
    "en": "Conservator appointed; effect on the existing power of attorney not characterised."
  }
}
~~~

# Event Types {#event-types}

The base URI for event types in this profile is:

`https://schemas.openid.net/secevent/dade/event-type/`

This document specifies five event types. Three further candidate event types
are described in {{DADE-EVENTS}} and are not specified here.

## principal-deceased

Event Type URI: `https://schemas.openid.net/secevent/dade/event-type/principal-deceased`

The `principal-deceased` event signals that the death of the Principal has been
recorded. It is the transition on which most of the rest of this profile
depends.

Two properties distinguish it from a simple assertion of fact. First, **a death
record can be wrong and can be withdrawn**; a Transmitter MUST be able to
correct one, and does so by sending a further `principal-deceased` event with
`record_status` set to `withdrawn` and `corrects` set to the `jti` of the
original. Second, **the proof of death is not always a death certificate**, and
the window in which it is not is precisely the window in which a family first
contacts a custodian.

Attributes:

- **record_status** - RECOMMENDED, JSON string: one of `recorded`, `amended` or
  `withdrawn`. If omitted, `recorded` is assumed. A Transmitter sending
  `amended` or `withdrawn` MUST include `corrects`.
- **date_of_death** - RECOMMENDED, JSON string: the date of death in the format
  YYYY-MM-DD, or, where the law of the jurisdiction permits a finding of
  presumed death, the date fixed by that finding.
- **death_type** - OPTIONAL, JSON string: one of `registered` (a civil registry
  holds the record), `certified` (a clinician certified it), `judicial` (a court
  declared or presumed it), or `reported` (asserted to the Transmitter without
  either).
- **proof** - OPTIONAL, JSON string: the artefact on which the record rests. This
  MUST be one of the following, or any other value mutually understood by the
  parties:
    - `death-certificate` - a certified or authenticated copy.
    - `abstract-of-death` - an abstract issued where a certificate is delayed.
      {{ROLES}} records a statute accepting this expressly for that reason.
    - `funeral-expense-attestation` - proof of payment of funeral expenses,
      accepted in at least one jurisdiction in place of a certificate.
    - `registry-record` - the Transmitter is itself the registry.
    - `court-order` - a judicial declaration of death.
- **registry_reference** - OPTIONAL, JSON string: an opaque reference to the
  record in the Transmitter's register, for later correlation.

The following example is non-normative.

~~~ json
{
  "iss": "https://registry.example.gov/",
  "jti": "a1b2c3d4e5f60718293a4b5c6d7e8f90",
  "iat": 1792108800,
  "aud": "https://platform.example.com/ssf",
  "txn": "dade-2026-0001",
  "sub_id": {
    "format": "principal",
    "principal_ref": "opaque:7f3c91a0e2",
    "jurisdiction": "US-IA"
  },
  "events": {
    "https://schemas.openid.net/secevent/dade/event-type/principal-deceased": {
      "record_status": "recorded",
      "date_of_death": "2026-10-02",
      "death_type": "registered",
      "proof": "death-certificate",
      "registry_reference": "IA-2026-114502",
      "initiating_authority": "registrar",
      "governing_law": { "jurisdiction": "US-IA", "as_at": "2026-10-14" },
      "event_timestamp": 1791936000
    }
  }
}
~~~

## principal-capacity-changed

Event Type URI: `https://schemas.openid.net/secevent/dade/event-type/principal-capacity-changed`

The `principal-capacity-changed` event signals that a determination has been
made about the Principal's capacity, or that an earlier determination has
ceased to hold. Both directions are carried by one event type because the
transition is symmetrical and because the reverse direction is load-bearing:
authority suspended on a finding of incapacity may revive when capacity returns.

The determination is **not** self-certifying and does not expire silently.
{{ROLES}} records statutory shelf lives on such findings ranging from two hours
to five years, after which the finding must be made again; a Transmitter that
knows the applicable limit SHOULD convey it in `expires_at`.

Attributes:

- **capacity_status** - REQUIRED, JSON string: one of `impaired` (a
  determination of incapacity has been made), `restored` (capacity has been found
  to have returned), or `contested` (the determination is under challenge).
- **determiner** - RECOMMENDED, JSON string: who made the determination. This
  MUST be one of `physician`, `psychologist`, `nurse-practitioner`,
  `physician-assistant`, `judge`, `governmental-official`, or `panel` where the
  law requires more than one.
- **scope** - RECOMMENDED, JSON string: one of `property`, `person`, or `both`.
  A determination of incapacity for financial purposes does not necessarily
  extend to health-care decisions, and conflating them over-reports.
- **finding_date** - OPTIONAL, JSON string: the date of the determination, in the
  format YYYY-MM-DD.
- **expires_at** - OPTIONAL, JSON number: the time, in seconds from
  1970-01-01T0:0:0Z as measured in UTC, after which the determination no longer
  holds without being made again. A Receiver MUST NOT treat a determination as
  continuing past this time.
- **objection** - OPTIONAL, JSON boolean: `true` where the Principal has objected
  to the determination and the law of the jurisdiction gives that objection
  effect.

The following example is non-normative.

~~~ json
{
  "iss": "https://ehr.example.org/",
  "jti": "11d0f2a37c9b48e5a6071829b3c4d5e6",
  "iat": 1792108900,
  "aud": "https://platform.example.com/ssf",
  "sub_id": {
    "format": "principal",
    "principal_ref": "opaque:7f3c91a0e2",
    "jurisdiction": "US-UT"
  },
  "events": {
    "https://schemas.openid.net/secevent/dade/event-type/principal-capacity-changed": {
      "capacity_status": "restored",
      "determiner": "physician",
      "scope": "both",
      "finding_date": "2026-10-11",
      "initiating_authority": "clinician",
      "governing_law": { "jurisdiction": "US-UT", "as_at": "2026-10-14" },
      "corrects": "0c9e8d7a6b5c4d3e2f10112233445566",
      "reason_admin": {
        "en": "Capacity found restored on re-examination; prior finding of 2026-08-02 no longer holds."
      }
    }
  }
}
~~~

## authority-changed

Event Type URI: `https://schemas.openid.net/secevent/dade/event-type/authority-changed`

The `authority-changed` event signals a change in the standing of a legal
authority held, or to be held, by a Holder over the Principal or their estate.
One event type carries the whole lifecycle, with `authority_status` selecting the
transition, because the parties, the role and the bounds are the same in each
case and only the transition differs.

Three of the `authority_status` values exist because the surveyed law requires
them and a two-state model cannot express them.

**`suspended` and `reinstated`.** An authority may be valid, temporarily
ineffective, and then effective again, with nothing issued or withdrawn at either
boundary. {{ROLES}} records a statute under which the appointment of a
conservator suspends an existing power of attorney, which is then "reinstated
upon termination of the conservatorship as a result of the principal regaining
capacity", and another under which a health-care authority commences, ceases and
resumes with successive clinical findings. A Receiver that models authority as
present or absent will either honour a dormant authority or refuse a revived one.

**`registered`.** In ten of the forty-four jurisdictions that record the point, a
power must be registered
or filed before it can be used, so there is a period in which the instrument
exists, is valid, and confers nothing. In one of them registration is
*constitutive* rather than procedural: the statute does not provide that the
power must be registered before use, it provides that the power is not created
unless registered. The `registration_effect` attribute distinguishes these,
because a Receiver that conflates them will either honour an authority that does
not exist or refuse one that does.

Attributes:

- **authority_status** - REQUIRED, JSON string: the transition. This MUST be one
  of:
    - `granted` - the authority has been conferred.
    - `registered` - a registry or court has completed the step that makes the
      authority effective, or that creates it; see `registration_effect`.
    - `suspended` - the authority continues to exist but is not currently
      effective.
    - `reinstated` - a suspended authority is effective again.
    - `scope-changed` - the bounds of the authority have moved; the authority
      has not ended.
    - `devolved` - the authority has passed from one Holder to another, for
      example to an alternate on the first Holder's forfeiture.
    - `terminated` - the authority has ended and will not revive.
- **holder** - RECOMMENDED, JSON object: identifies the Holder. It MUST contain a
  `holder_ref` (JSON string, an opaque reference as described in
  {{principal-subject}}) and MAY contain `holder_type` (one of `natural-person`,
  `legal-person`, `public-office`).
- **artefact** - OPTIONAL, JSON string: what evidences the authority. This MUST
  be one of `letters`, `grant`, `certificate-of-inheritance`, `court-order`,
  `instrument`, `affidavit`, `certification-of-trust`, `register-entry`,
  `platform-record`, or **`none`**. The last value is not an error: in a
  substantial minority of jurisdictions the authority arises with no artefact at
  all.
- **scope** - OPTIONAL, JSON object: the bounds of the authority as stated on its
  face. It MAY contain `limits` (JSON array of strings), `monetary_ceiling` (JSON
  object with `amount` as a JSON number and `currency` as an ISO 4217 code), and
  `co_holders` (JSON object with `count` as a JSON number and `acting` as one of
  `jointly`, `independently`, or `majority`). Amounts MUST be expressed in the
  currency of the governing jurisdiction and MUST NOT be converted.
- **registration_effect** - OPTIONAL, JSON string: present where
  `authority_status` is `registered`. One of `activates` (the instrument already
  existed and registration makes it effective) or `creates` (the authority does
  not exist until registration).
- **revival** - OPTIONAL, JSON string: present where `authority_status` is
  `suspended`. One of `automatic` (the authority revives on a condition without
  further order, so the suspension is known in advance not to be terminal),
  `order-required`, or `none`.
- **cause** - OPTIONAL, JSON string: why the transition occurred. This MUST be
  one of `death`, `revocation`, `court-appointment`, `court-order`, `conviction`,
  `administrative-finding`, `non-exercise`, `expiry`, `purpose-fulfilled`,
  `resignation`, `capacity-restored`, or any other value mutually understood by
  the parties.
- **predecessor** - OPTIONAL, JSON object: present where `authority_status` is
  `devolved`. Identifies the Holder from whom the authority passed, with the same
  structure as `holder`.

A Transmitter SHOULD send `reinstated` when a suspension it reported has ended,
rather than leaving a Receiver to infer it from a `principal-capacity-changed`
event, because the inference is jurisdiction-dependent.

The following example is non-normative. It shows a power of attorney suspended by
the appointment of a conservator, with the suspension marked as one that will
revive automatically.

~~~ json
{
  "iss": "https://court.example.gov/",
  "jti": "99aa88bb77cc66dd55ee44ff33221100",
  "iat": 1792109000,
  "aud": "https://platform.example.com/ssf",
  "txn": "dade-2026-0042",
  "sub_id": {
    "format": "principal",
    "principal_ref": "opaque:7f3c91a0e2",
    "jurisdiction": "US-IA"
  },
  "events": {
    "https://schemas.openid.net/secevent/dade/event-type/authority-changed": {
      "authority_status": "suspended",
      "canonical_role": "financial-poa-durable",
      "holder": { "holder_ref": "opaque:b21c7e", "holder_type": "natural-person" },
      "artefact": "instrument",
      "cause": "court-appointment",
      "revival": "automatic",
      "initiating_authority": "court",
      "governing_law": { "jurisdiction": "US-IA", "as_at": "2026-10-14" },
      "effect_unspecified": false,
      "reason_admin": {
        "en": "Conservator appointed; power of attorney suspended and revives if capacity is regained."
      }
    }
  }
}
~~~

## direction-recorded

Event Type URI: `https://schemas.openid.net/secevent/dade/event-type/direction-recorded`

The `direction-recorded` event signals that the Principal has lodged a direction
with a custodian about post-mortem access to their accounts or data, or has
withdrawn one.

**This is not a variant of `authority-changed`, and the distinction is the
reason the event exists.** A direction is not necessarily a grant. In one
surveyed jurisdiction the deceased's data-protection rights are exercisable by an
interested person *unless the deceased forbade it in writing to the controller*,
and that prohibition binds. In another, directions may permit or forbid and are
lodged with the controller concerned, require the data subject's specific consent,
and expressly may not result from their mere acceptance of the terms of use; a
terms-of-service clause cutting across that right is void. An event vocabulary
that can only say that someone now
holds an authority cannot carry either, and a Receiver implementing only the
permitting case silently mis-implements the prohibiting one.

The addressee matters as much as the content. Where the law gives a prohibition
effect by virtue of its having been lodged **with the controller**, the custodian
is not a relying party assessing someone else's instrument; it is the party to
whom the instrument was given.

Attributes:

- **direction_status** - REQUIRED, JSON string: one of `recorded` or `withdrawn`.
  A Transmitter sending `withdrawn` SHOULD include `supersedes`.
- **effect** - REQUIRED, JSON string: one of `permit` or **`forbid`**. The
  `forbid` value is a first-class direction and MUST NOT be represented as the
  absence of a `permit`.
- **lodged_with** - RECOMMENDED, JSON string: an identifier for the custodian or
  controller with which the direction was lodged, where the law attaches
  significance to the addressee.
- **designee** - OPTIONAL, JSON object: where the direction names a person to
  act, with the same structure as `holder` in `authority-changed`.
- **scope** - OPTIONAL, JSON object: what the direction reaches. It MAY contain
  `assets` (JSON array of strings, for example `content`, `catalogue`,
  `account-control`, `deletion`) and `exclusions` (JSON array of strings).
- **precedence** - OPTIONAL, JSON string: the direction's rank against other
  instruments, where the governing law states one. One of
  `overrides-other-records` (the direction prevails over a contrary direction in
  a will, trust, power of attorney or other record) or `subordinate`.
- **revocable** - OPTIONAL, JSON boolean: whether the Principal may withdraw the
  direction at any time. Where the law requires that the custodian's tool permit
  modification at any time as a condition of the direction's precedence, a
  Transmitter SHOULD set this to `true` and set `precedence` accordingly.

The following example is non-normative. It shows a prohibition.

~~~ json
{
  "iss": "https://platform.example.com/",
  "jti": "cc00dd11ee22ff33445566778899aabb",
  "iat": 1792109100,
  "aud": "https://executor-service.example.net/ssf",
  "sub_id": {
    "format": "principal",
    "principal_ref": "opaque:7f3c91a0e2",
    "jurisdiction": "IT"
  },
  "events": {
    "https://schemas.openid.net/secevent/dade/event-type/direction-recorded": {
      "direction_status": "recorded",
      "effect": "forbid",
      "lodged_with": "https://platform.example.com/",
      "scope": { "assets": ["content", "catalogue"] },
      "revocable": true,
      "initiating_authority": "principal",
      "governing_law": { "jurisdiction": "IT", "as_at": "2026-10-14" },
      "reason_user": {
        "it": "Hai chiesto che i tuoi dati non siano resi accessibili ad altri dopo la tua morte."
      }
    }
  }
}
~~~

## authority-refused

Event Type URI: `https://schemas.openid.net/secevent/dade/event-type/authority-refused`

The `authority-refused` event signals that a custodian has declined to honour an
authority presented to it, and states the ground.

**This event travels in the opposite direction to every other event in this
profile**, and it exists because at least one legislature already requires it. In
the jurisdiction concerned, a person refusing to accept the authority of a
guardian or conservator must, within ten days of the refusal, report the refusal
and the reason for it to the court that issued the letters of office, where it is
treated as a grievance. The custodian is the Transmitter and the issuing
authority is the Receiver.

Because SSF Streams are unidirectional, a deployment supporting this event
establishes a Stream in which the issuing authority is the Receiver, distinct
from any Stream over which that authority transmits.

A refusal is a legitimate outcome and not an error. Several of the surveyed
statutes enumerate the grounds on which an authority may lawfully be refused, and
two enumerate grounds on which it may **not** be; the `grounds` registry in
{{refusal-grounds}} is drawn from them.

Attributes:

- **grounds** - REQUIRED, JSON array of strings: one or more values from the
  registry in {{refusal-grounds}}, or any other value mutually understood by the
  parties. A Transmitter MUST NOT send an empty array.
- **holder** - RECOMMENDED, JSON object: the party whose authority was refused,
  with the same structure as `holder` in `authority-changed`.
- **presented_at** - OPTIONAL, JSON number: the time the authority was presented
  to the custodian, in seconds from 1970-01-01T0:0:0Z as measured in UTC. Where a
  statute imposes a deadline for reporting a refusal, this is the time from which
  it runs.
- **artefact** - OPTIONAL, JSON string: what was presented, using the values of
  `artefact` in `authority-changed`.
- **report_deadline** - OPTIONAL, JSON number: the time by which the governing law
  requires the refusal to be reported, where it imposes one.
- **remediable** - OPTIONAL, JSON boolean: whether the custodian would honour the
  authority if the ground were addressed. A refusal for want of evidence of a
  contingency is remediable; one resting on knowledge of abuse is not.

The following example is non-normative.

~~~ json
{
  "iss": "https://platform.example.com/",
  "jti": "5566778899aabbccddeeff0011223344",
  "iat": 1792109200,
  "aud": "https://court.example.gov/ssf",
  "txn": "dade-2026-0042",
  "sub_id": {
    "format": "principal",
    "principal_ref": "opaque:7f3c91a0e2",
    "jurisdiction": "US-KS"
  },
  "events": {
    "https://schemas.openid.net/secevent/dade/event-type/authority-refused": {
      "grounds": ["abuse-report-made"],
      "holder": { "holder_ref": "opaque:b21c7e", "holder_type": "natural-person" },
      "artefact": "letters",
      "presented_at": 1792022800,
      "report_deadline": 1792886800,
      "remediable": false,
      "initiating_authority": "custodian",
      "governing_law": { "jurisdiction": "US-KS", "as_at": "2026-10-14" },
      "reason_admin": {
        "en": "Refused: a report under the adult protective services statute has been made naming the guardian."
      }
    }
  }
}
~~~

# Subjects and the Principal Subject Format {#principal-subject}

Events in this profile concern a person who may be deceased. {{RFC9493}} defines
no Subject Identifier Format for such a person, and the formats it does define
are a poor fit: an `email` or `phone_number` identifier for a deceased person is
both likely to be reassigned and unusually sensitive, and correlating a decedent
across a civil registry and a platform is precisely the hazard the privacy
considerations of {{RFC8417}}, {{RFC8935}} and {{RFC8936}} describe.

This document defines the `principal` Subject Identifier Format.

- **format** - REQUIRED, JSON string: MUST be `principal`.
- **principal_ref** - REQUIRED, JSON string: an opaque identifier for the
  Principal. It MUST be scoped to the Transmitter–Receiver pair, MUST NOT be
  derived from a government identifier by a reversible transformation, and MUST
  NOT be reused for a different Principal.
- **jurisdiction** - OPTIONAL, JSON string: the Principal's domicile, where the
  Transmitter knows it, as an ISO 3166-2 or ISO 3166-1 alpha-2 code. This assists
  a Receiver in selecting the law against which to evaluate an event, but does
  not displace `governing_law`.

Where the Holder rather than the Principal is the subject of interest, the Holder
is conveyed in the `holder` attribute of the event rather than as the SET's
subject. The subject of every event in this profile is the Principal, so that a
Receiver can correlate the whole sequence concerning one person on `sub_id`
alone.

# Receiver Processing {#receiver-processing}

A Receiver MUST NOT treat any event in this profile as an instruction. The
decision to grant, suspend or deny access remains the Receiver's, taken under its
own terms and the applicable law.

Three constraints are specific to this subject matter.

**An absence of events is not an absence of change.** At least one surveyed
statute provides expressly that failure to register a document, or to register a
revocation, does not affect its validity. A Receiver that has received no event
has learned something about the Stream and nothing about the world, and MUST NOT
treat a quiet Stream as positive evidence that an authority continues.

**Some deliveries are constitutive.** In at least one jurisdiction the forfeiture
of an authority on the Holder being charged with an offence takes effect only once
those charges are "known to a third party", and in another the priority of an
agent over a court-appointed guardian holds only while the agent is "known to the
health care provider to be available and willing". Where the governing law makes
the legal effect of a transition contingent on a party's knowledge, the delivery
of the SET may be what causes the effect to attach. Both Transmitter and Receiver
SHOULD retain delivery acknowledgements in such deployments, as evidence rather
than as transport state.

**Latency can be dispositive.** At least one surveyed authority is forfeited if
it is not exercised within twenty-four hours of the Holder being notified of the
death, or forty hours of the death, whichever is earlier. Where a deployment
carries events bearing on such an authority, delivery SHOULD use the push
mechanism of {{RFC8935}}; a poll-based Stream on a daily cadence cannot serve a
deadline of this kind.

# Refusal Grounds Registry {#refusal-grounds}

The following values are defined for the `grounds` attribute of
`authority-refused`. They are drawn from statutes that enumerate the grounds on
which an authority may lawfully be refused.

- `actual-knowledge-invalid` - the custodian has actual knowledge that the
  authority or the instrument is void, invalid, terminated or revoked.
- `good-faith-belief-invalid` - the custodian believes in good faith that the
  authority is not valid or does not extend to the act requested. At least one
  statute makes this ground available whether or not a certification or opinion
  of counsel was requested or provided, so a Receiver MUST NOT assume that
  supplying further evidence removes it.
- `exceeding-authority` - the custodian has actual knowledge or a reasonable
  belief that the Holder is exceeding or improperly exercising the authority.
- `abuse-known` - the custodian has actual knowledge that the Principal is
  subject to physical or financial abuse, neglect, exploitation or abandonment by
  the Holder.
- `abuse-report-made` - the custodian has made, or knows that another has made, a
  report of such abuse to the competent authority.
- `inconsistent-with-law` - performing the transaction would be inconsistent with
  other applicable law.
- `pending-proceeding` - a judicial proceeding construing the authority or
  reviewing the Holder's conduct is pending.
- `contingency-unproven` - the authority is conditioned on a contingency and
  neither a certification nor evidence of its occurrence has been presented.
- `not-otherwise-obliged` - the custodian would not have been required to engage
  in the transaction with the Principal in the same circumstances.

Two grounds are expressly **prohibited** by at least one of the surveyed statutes
and MUST NOT be sent as values of `grounds`:

- a refusal resting *exclusively* on the age or date of execution of the
  instrument; and
- a refusal resting *exclusively* on a requirement that a different form of
  instrument be used.

A Receiver that is an issuing authority SHOULD treat the receipt of a refusal on
a prohibited ground, or the absence of any ground, as a matter for its own
process.

# Privacy Considerations

The subject of these events is a person who is dead or has lost capacity, and who
therefore cannot consent to the transmission, object to it, or exercise a right
in respect of it. Several jurisdictions nonetheless protect a decedent's data,
and one surveyed jurisdiction protects it as an exercisable right of interested
persons.

- Subject identifiers MUST be opaque and scoped per Transmitter–Receiver pair
  ({{principal-subject}}). Correlation of a decedent across registries and
  platforms is the principal privacy hazard of this profile.
- A Transmitter MUST NOT include a cause of death, a diagnosis, or clinical
  detail. `principal-capacity-changed` conveys that a determination was made,
  by whom, and in respect of what, and nothing about the Principal's condition.
- `reason_user` SHOULD be omitted where the Principal is deceased, since there is
  no end user to read it, except where the Receiver will show it to a surviving
  Holder.
- A Stream carrying these events reveals a death to its Receiver before the
  family may have told anyone. Transmitters SHOULD restrict such Streams to
  Receivers with a legal basis for the notification.

# Security Considerations

The security considerations of {{RFC8417}}, {{SSF}}, {{RFC8935}} and {{RFC8936}}
apply.

A false `principal-deceased` event is an account-takeover primitive: it may cause
a Receiver to grant a putative Holder access to a living person's accounts.
Receivers SHOULD require that such events originate from a Transmitter with a
basis for the assertion, SHOULD weigh `initiating_authority` and `proof`, and
SHOULD NOT act on `death_type` of `reported` alone. The ability to send
`record_status` of `withdrawn` limits the damage but does not prevent it, since
the correction arrives after the access.

`authority-changed` with `authority_status` of `granted` is the same primitive
one step removed. The `operation-of-law` value of `initiating_authority` is the
weakest assertion in this profile — nobody declared the transition — and a
Receiver SHOULD NOT treat it as sufficient on its own for an irreversible action
such as deletion.

# IANA Considerations

This document requests the registration of five event types in the "Security
Event Token Event Types" registry, under the base URI
`https://schemas.openid.net/secevent/dade/event-type/`:
`principal-deceased`, `principal-capacity-changed`, `authority-changed`,
`direction-recorded` and `authority-refused`.

This document also requests the registration of the `principal` Subject
Identifier Format in the "Security Event Token Subject Identifier Formats"
registry established by {{RFC9493}}.

--- back

# Use Cases
{:numbered="false"}

## A family contacts a platform after a death
{:numbered="false"}

A civil registry transmits `principal-deceased`. The platform does not grant
anything on that alone; it learns that a claim is now possible and that its
inactivity timers should not run. When a Holder later presents a grant, the
platform has already correlated the death and can evaluate the authority against
the jurisdiction the registry named.

## A power of attorney goes dormant and comes back
{:numbered="false"}

A court transmits `authority-changed` with `authority_status` of `suspended`,
`cause` of `court-appointment` and `revival` of `automatic`. The platform stops
honouring the agent without revoking anything or asking the agent to re-enrol.
Months later the same court transmits `reinstated`, and the agent resumes. No
instrument changed at either boundary, and without the events the platform would
have had no way to learn of either.

## A custodian says no, and the court finds out
{:numbered="false"}

A platform refuses letters of office it has reason to believe are being misused
and transmits `authority-refused` with `grounds` of `abuse-report-made` to the
issuing court, within the period the governing law allows. The court treats it as
a grievance. The platform has discharged a statutory duty it would otherwise have
had to discharge on paper, and the refusal has reached the only party able to act
on it.

## A prohibition is honoured
{:numbered="false"}

A user lodges a direction forbidding post-mortem disclosure. The platform records
it and transmits `direction-recorded` with `effect` of `forbid` to an estate
service the user also uses. When the user dies, the estate service already knows
not to ask.

# Acknowledgments
{:numbered="false"}

The problem this profile addresses is set out in {{DADE-PAPER}}, and the author
thanks its contributors and the members of the OpenID Foundation's Death and the
Digital Estate Community Group. The jurisdictional survey underlying the
requirements is {{ROLES}}.

# Notices
{:numbered="false"}

Copyright (c) 2026 the author. This document is a draft offered for discussion
and carries no status within the OpenID Foundation.

# Document History
{:numbered="false"}

-00

- Initial draft. Defines the `principal-deceased`, `principal-capacity-changed`,
  `authority-changed`, `direction-recorded` and `authority-refused` event types, the
  `principal` subject identifier format, and the refusal grounds registry.
- Establishes the facts-not-effects rule: every event names the law against which its
  consequence is to be evaluated, and a Transmitter that will not characterise that
  consequence says so with `effect_unspecified`.
- Three further candidate event types — `authority-lapse-pending`, `authority-presented`
  and `authority-accepted` — are raised in the accompanying DADE Event Catalog and are not
  specified here.
