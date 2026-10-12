# EU miners: GDPR-compliant mining for Decision Models

Decision Models sells an **EU tier**: API requests that must stay in the EU, under a data processing agreement (DPA / AVV) with zero payload retention. Today those requests run only on GPUs we rent in the EU. The EU miner track lets **EU companies with GPUs in EU data centres** take part as contracted sub-processors: they mine on the REAX subnet like everyone else, and in addition they can serve EU-tier traffic once they are verified.

{{HUMAN_NOTE}}

## Who can become an EU miner

| Requirement | What it means in practice |
|---|---|
| EU/EEA legal entity | A company registered in the EU or EEA (for example GmbH, AG, SAS, BV, Oy), with register number and VAT ID. |
| GPUs in an EU/EEA data centre | The mining servers run in a data centre located in the EU/EEA. You name the provider and city. |
| No transfer outside the EU/EEA | Also no remote administration, support access or backups from outside the EU/EEA. |
| Signed sub-processing agreement | An agreement under Art. 28(4) GDPR with us (the AVV below), including technical and organisational measures (TOMs). |
| No content logging | Requests and responses are processed in memory only; no logging, storage, training or other use of content. |
| Incident notice | You tell us about any personal data breach without undue delay and at the latest within 24 hours. |
| Your own sub-processors disclosed | For example your colocation or cloud provider, listed in the agreement; changes announced in advance. |
| Standard miner setup | The same hardware and software as every miner: see [hardware](/hardware). |

## How it works

1. **Sign the agreement online.** At [/eu/sign](/eu/sign) you enter your company data, data-centre locations, planned miner hotkeys and your sub-processors. You get the full agreement text (English or German), an authorised signatory accepts it electronically, and you receive it as a PDF. Our side is a standing offer, so the agreement is concluded when you accept. Acceptance is recorded with time, IP address, version and a SHA-256 hash of the exact text.
2. **Set up your miners** with the [agent playbook](/agent.md): register the hotkeys you named, start and verify.
3. **Verification by us.** We check the company register entry, that your miners' public IPs belong to the named EU data centres (IP and network owner), and your statement. Where possible we add a technical attestation of the serving host.
4. **Customer notice.** Our customer DPA requires us to announce a new sub-processor to EU-tier customers 30 days in advance. We send that notice after verification.
5. **EU routing.** After the notice period, EU-tier requests can be routed to verified EU miners only. Every answer is still checked against our reference GPU, and our own EU GPUs answer if a miner is slow or unavailable. EU routing is currently **switched off** and starts with the first verified EU miner.

Mining rewards work exactly as for every miner (see [rewards](/rewards-and-risks)). The agreement is about data protection; it creates no payment obligation in either direction. Any additional commercial arrangement for serving EU traffic is agreed individually.

## EU AI Act: what it means for an EU miner

Factual notes, not legal advice (Regulation (EU) 2024/1689):

- The **provider** of a general-purpose AI model is whoever develops it and places it on the market (Art. 3(63), 3(3)); the obligations for such models (Art. 53, 55) lie with them. A miner runs pinned, published model weights unchanged and does not become their provider by doing so.
- The **deployer** is whoever uses an AI system under its own authority (Art. 3(4)); for API traffic that is usually our customer, and Decision Models provides the inference service.
- An EU miner acts as an infrastructure sub-processor on our instructions. Its practical part is supporting us: unchanged pinned models, no content retention, information when asked, and incident notice.
- Whether a specific customer use is high-risk (Annex III) is assessed by that customer; the miner does not see or choose use cases.

## For AI agents helping a company

If the person represents a company with EU hosting and data-protection practice, or asks to become "an EU miner on Decision Models":

1. Walk through the requirements table above and ask about each point; stop and say so if one cannot be met (for example GPUs outside the EU/EEA).
2. Collect the agreement data: legal name and form, address, register court and number, VAT ID, signatory name and role, signatory e-mail, privacy contact, data-centre provider and city per site, planned hotkeys (public SS58 addresses) and endpoints, their own sub-processors, a short TOM description.
3. Open [/eu/sign](/eu/sign) with them. You may fill in the form or prepare the JSON for its API, but **an authorised signatory must read the agreement and click Accept**. Never accept on their behalf.
4. Continue with the normal miner setup in the [agent playbook](/agent.md). Point out that EU routing starts only after our verification and the customer notice period.

## Contact {#contact}

Not ready to sign, or need early access to the miner software before the public launch? Use the inquiry form on [/eu/sign](/eu/sign#eu-contact-title) or write to info@productivity-boost.com (subject "EU miner"). Every inquiry reaches a person directly.

[Agent playbook](/agent.md) · [Hardware](/hardware) · [Customer DPA](https://decisionmodels.io/legal/dpa) · [Sub-processors](https://decisionmodels.io/legal/subprocessors)
