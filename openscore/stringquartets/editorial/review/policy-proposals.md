# Policy references and proposed clarifications

Status: proposals for the project editors. None of the text below has been adopted as a new rule or published to the guidelines website. The scores, existing editorial decisions and excerpt images are unchanged by this consolidation.

The authority is [Notes for Transcribers](https://fourscoreandmore.org/scores-of-scores/notes-for-transcribers/), checked on 26 October 2026, with the page labelled “Last Updated: October 2026”. `assets/policy-codes.json` is a navigation index, not a second policy document. Its URLs deliberately use the verified source page; this build does not invent per-rule anchors.

The current page already addresses rest grouping (T3), tuplets (T4), measured tremolo (T5), historical cello octave notation (C2.3.1), clef readability (C3), clef conversion (C4), and standard tempo abbreviations (D3). Those subjects do not need duplicate general policies in each edition.

## PROPOSAL-STABLE-REFERENCES

**Target:** the guideline's maintenance and citation system.

**Reason:** an older cached retrieval and the current retrieval used different numbering for some rules, while both carried the same month-level update label. The current W section is unnumbered. A code alone therefore cannot always identify the wording used when an edition was reviewed.

**Suggested addition:** give each rule a permanent HTML anchor and publish an explicit revision identifier or date. Retain a change log when an existing code changes meaning, and provide an old-to-new mapping when renumbering is unavoidable. Give the W paragraph an explicit number if letter-number references are required throughout. Do not silently treat old T3 references as references to the current T3.

**Implementation here:** metadata records the source URL, retrieval date and displayed version label. New references use the current numbering. W is a section reference, not an invented W1.

## PROPOSAL-NAVIGATION

**Target:** a future navigation rule; no official code assigned here.

**Example:** `sq8071278`, ED-011, Scherzo ending.

**Suggested addition:** permit an explicit destination or ending label when it makes an unambiguous source return instruction readable in the score and parts. Document the supplied label and verify the return path, including the intended treatment of repeats. Where the destination or repeat behavior is uncertain, leave a question for review rather than choosing a route silently.

**Current handling:** the existing Fine remains a local accepted choice. G7 is reviewer context; it is not represented as a navigation-specific rule.

## PROPOSAL-TUPLET-SCOPE

**Target:** T4.2.

**Examples:** `sq8071278`, ED-013 and ED-016.

**Suggested clarification:** define what counts as one continuous tuplet passage and when its first indication must be renewed. Address short pairs of groups, interruptions, new sections and system breaks. Specify whether isolated reminders later in a passage may be retained, or should be moved to the beginning of the relevant group.

**Current handling:** ED-012 follows the first-group convention. ED-013 retains numerals on two short groups; ED-016 retains a numeral on the second group while the first is unnumbered. Their earlier decisions are preserved, with policy-alignment questions recorded. No numeral or rhythm was changed during consolidation.

## PROPOSAL-ORNAMENT-LINES

**Target:** optional clarification under O1/O2 or an example under G2.

**Example:** `sq10502527`, ED-002, viola trill.

**Suggested clarification:** state whether a native ornament's default extension line may be retained when the source prints only the ornament sign. Require the documented extent, auxiliary accidental and closing notes to remain unchanged; a default line must not supply an uncertain continuation.

**Current handling:** the existing finite extension remains a local decision, with G2 and O1 as relevant references. The record continues to explain the observed source-to-edition difference.

## PROPOSAL-SOURCE-COURTESIES

**Target:** S2.

**Suggested clarification:** state whether S2 is unconditional even when the source explicitly repeats an accidental on a tied continuation, or whether an editor may retain such a source courtesy in a documented exception. If S2 is unconditional, record the suppression as policy application rather than a source omission to repair.

**Migration check:** a previously discussed Bartók No.2 I.88 repair deliberately retained a source courtesy sharp. That package is not present in this consolidation's local input set. When imported, its actual record and score should be checked against S2; do not automatically call it compliant or remove the accidental during data migration.

## PROPOSAL-SOURCE-QUESTIONS

**Target:** the relationship between G1 and B1–B3.

**Suggested clarification:** distinguish an adopted reading enclosed in source editorial brackets from an unresolved source question, queried accidental or alternative reading. Preserve attribution and uncertainty when a source raises a question; removing bracket typography must not silently turn a queried reading into a settled one.

**Migration check:** imported records about source queries should retain their separate review status. This clarification proposes no new pitch decisions.

## Passage checks already covered by the guide

Some Grosse Fuge tenor-to-bass substitutions refer to C3, but their older notes do not document the ledger-line and duration assessment. Their accepted decisions remain intact and are labelled local decisions rather than automatic default applications. The two rest-grouping records likewise establish equal duration, but do not by themselves prove the exact meter-default grouping required by T3. These are checks of local applications, not proposals to replace C3 or T3.

## Maintainer note

Policy review status is separate from musical review status. `covered`, `local_decision`, `clarification_needed` and `conflict` describe alignment with the guideline. They do not turn an accepted editorial choice into an unresolved transcription error, nor a repaired correction into an uncorrected score. Any future musical change needs its own review and native-file validation.
