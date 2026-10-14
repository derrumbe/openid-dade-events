# OpenID Death and the Digital Estate Event Profile (DADE Events)

A proposed profile of the [Shared Signals Framework][ssf] for the legal transitions that
govern access to a person's accounts when that person dies or loses capacity.

Where other Shared Signals event sets describe the security state of a session, an account
or an environment, DADE describes **who may lawfully act for a person, and on what
standing**: a death recorded, a finding of incapacity or its reversal, the grant,
registration, suspension, reinstatement, termination and devolution of an authority over
the person or their estate, a direction the person lodged with a custodian, and a
custodian's refusal to honour an authority presented to it.

The event vocabulary is drawn from a survey of **56 jurisdictions across 24 countries**
([Digital Estate Roles][roles]), in which every claim is cited to primary law with a
retrieval date.

## Facts, not effects

DADE events carry facts, **not their legal consequences**, and that is a requirement rather
than reticence.

A court appoints a conservator over the property of someone who had granted a power of
attorney. Across seven US states that one transition has five different effects on the
existing power: in Virginia the agency continues; in West Virginia and Kentucky it
terminates; in Missouri the court allocates functions between the two fiduciaries; in
Nebraska and Kansas the conservator acquires the principal's own power to revoke it; and in
Iowa the power is *suspended* and later *reinstated* if the principal regains capacity.

An event asserting "the power of attorney is terminated" would be wrong in five of those
seven. An event asserting "a conservator was appointed over this principal's property, under
the law of Iowa, as at this date" is correct in all of them, and leaves the consequence to
whoever is entitled to draw it. Hence `governing_law` on every event, and
`effect_unspecified` for a Transmitter that will not characterise the result.

## Documents

| Document | Source |
| --- | --- |
| OpenID DADE Event Profile 1.0 — draft 00 | [`openid-dade-events-1_0.md`](openid-dade-events-1_0.md) |
| DADE Event Catalog — all candidate events | [`EVENT-CATALOG.md`](EVENT-CATALOG.md) |
| DADE Event Reference — per-event detail, the statute behind each claim, and examples | [`dade-event-reference.html`](dade-event-reference.html) |

All three are published at <https://derrumbe.github.io/openid-dade-events/>:

| Page | Link |
| --- | --- |
| Specification | <https://derrumbe.github.io/openid-dade-events/> |
| Event catalog | <https://derrumbe.github.io/openid-dade-events/event-catalog.html> |
| Event reference | <https://derrumbe.github.io/openid-dade-events/dade-event-reference.html> |

The specification is written in [kramdown-rfc][kr] markdown and rendered with
[xml2rfc][xr], the same toolchain used by the Shared Signals specifications.

## Event types

Five event types are specified in draft 00:

| Event type | Signals |
| --- | --- |
| `principal-deceased` | A death has been recorded — and can be withdrawn |
| `principal-capacity-changed` | A capacity determination was made, or has ceased to hold |
| `authority-changed` | An authority was granted, registered, suspended, reinstated, re-scoped, devolved or terminated |
| `direction-recorded` | The principal lodged a direction about post-mortem access — permitting **or forbidding** |
| `authority-refused` | A custodian declined to honour an authority, and states the ground |

Three further candidates — `authority-lapse-pending`, `authority-presented` and
`authority-accepted` — are raised in the Event Catalog and not specified here. The
[DADE Event Reference](https://derrumbe.github.io/openid-dade-events/dade-event-reference.html)
details all eight, each with the statute that makes the claim necessary.

Draft 00 also defines a **`principal` Subject Identifier Format**, because [RFC 9493][9493]
defines none for a person who has died, and the formats it does define fit badly: an
`email` or `phone_number` identifier for a decedent is both likely to be reassigned and
unusually sensitive.

## Why these shapes

Three design choices in the draft exist because the surveyed law leaves no alternative.

**An authority can be dormant.** `authority_status` carries `suspended` and `reinstated`
because an authority may be valid, temporarily ineffective, and effective again, with
nothing issued or withdrawn at either boundary. A Receiver modelling authority as present
or absent will either honour a dormant authority or refuse a revived one.

**An instrument can be valid and confer nothing.** In ten of the forty-four jurisdictions that
record the point, a
power must be registered before use; in one, registration is *constitutive* rather than
procedural — the power is not created unless registered. `registration_effect`
distinguishes them.

**Most of the world issues no document at all.** In 16 of the 24 countries surveyed the
heirs hold the estate from the moment of death, with no artefact and nobody declaring
anything. `artefact: none` and `initiating_authority: operation-of-law` are how that is
said.

## Building

Requires `kramdown-rfc` (Ruby) and `xml2rfc` (Python):

```sh
gem install kramdown-rfc
pip install xml2rfc markdown

make all       # -> build/openid-dade-events-1_0.{html,txt}
make publish   # -> public/index.html
make clean
```

`make all` also produces a `.docx` when `pandoc` is available.

`kramdown-rfc` resolves the normative references by fetching reference XML from
`bib.ietf.org` into a local `.refcache/`. Some sandboxed or proxied environments deny that
host, which fails the build with a `403 Forbidden` from `net/http` rather than anything
wrong in the source; CI reaches it. The markdown itself converts without network access —
only the reference resolution needs it.

## Status

This is an independent working draft prepared as input to the OpenID Foundation Shared
Signals Working Group and the [Death and the Digital Estate][dade] community group. **It is
not a publication of the OpenID Foundation** and confers no standards status. It references
OpenID Foundation specifications, which are subject to the Foundation's intellectual
property and copyright policies.

It is **not legal advice**. The statutory grounding is sourced and dated in
[Digital Estate Roles][roles]; law changes, and every citation there records its retrieval
date.

[ssf]: https://openid.net/specs/openid-sharedsignals-framework-1_0.html
[9493]: https://www.rfc-editor.org/rfc/rfc9493.html
[roles]: https://xebecstudios.org/research/digital-estate-roles/
[dade]: https://openid.net/wg/digital-estate/
[kr]: https://github.com/cabo/kramdown-rfc
[xr]: https://github.com/ietf-tools/xml2rfc
