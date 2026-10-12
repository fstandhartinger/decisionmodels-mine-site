# Sub-Processing Agreement for EU Miners (Art. 28(2) and (4) GDPR)

Decision Models — REAX network (Bittensor subnet 92)

Version {{version}} · Agreement ID {{agreement_id}}

*The German version prevails if the language versions differ (section 17.5).*

## Parties

**Operator ("Operator", "Processor" or "we")**

productivity-boost.com Betriebs UG (haftungsbeschränkt) & Co. KG, Reichenberger Str. 2, 94036 Passau, Germany, Amtsgericht Passau HRA 12725, represented by its general partner productivity-boost.com UG (haftungsbeschränkt) (Amtsgericht Passau HRB 8453), itself represented by its managing director Florian Standhartinger. Brand: Decision Models (decisionmodels.io). Contact for this agreement: info@productivity-boost.com.

**Miner ("Miner" or "Sub-Processor")**

{{miner_company}} ({{miner_legal_form}}), {{miner_address}}, {{miner_country}}, register entry (if any): {{miner_register}}, VAT ID: {{miner_vat_id}}, represented by {{signatory_name}} ({{signatory_role}}), e-mail {{signatory_email}}.

Contact for data protection at the Miner: {{privacy_contact}}.

## Record of conclusion

| Item | Value |
| --- | --- |
| Agreement ID | {{agreement_id}} |
| Version of the text | {{version}} |
| Accepted on (UTC) | {{accepted_at}} |
| SHA-256 of the completed text accepted by the Miner (including its entries and the Annexes; for hashing, the fields Agreement ID, Accepted on and SHA-256 show the marker "assigned on acceptance" in square brackets) | {{text_sha256}} |

The text of this agreement published on mine.decisionmodels.io is a standing offer by the Operator to companies that meet the requirements of section 3.1. The Operator agrees in advance that the Miner makes the entries in the form (party data, Annex 2 Part B, Annex 3 and Annex 4); these entries do not change sections 1 to 17 or Annex 2 Part A, which prevail in case of conflict, and the use of the Locations, Endpoints, hotkeys and sub-processors entered requires the Operator's confirmation under sections 3.6 and 8.1. The Miner accepts the offer by the electronic declaration of an authorised signatory (name, role, company, e-mail address and the confirmation "I am authorised to represent the company named above"). The agreement is concluded when the acceptance is received by the Operator's system. Verification of the Miner (section 3.5) is not a condition for the conclusion of this agreement; it is a condition for routing (Preamble (D), section 2.1) and for the Operator's confirmation of Locations, Endpoints, hotkeys and sub-processors (sections 3.6 and 8.1). The acceptance is recorded with timestamp (UTC), IP address, version and the SHA-256 hash of the completed text displayed to the signatory. The Miner receives the complete agreement as a PDF for download immediately on acceptance; the Operator sends a further copy by e-mail on request. The agreement is thereby concluded in writing in electronic form within the meaning of Art. 28(9) GDPR.

## Preamble

(A) The Operator provides the Decision Models inference service (typed-decision inference: a state, a question and answer options go in, probabilities come out). For its API customers the Operator acts as processor under its Data Processing Agreement (version 1.2 or later, "Customer DPA").

(B) The Operator may in future route requests of its EU tier to independent companies that operate GPU hardware in data centres in the EU and take part in the REAX network (Bittensor subnet 92) as miners. A Miner that receives such requests processes personal data on behalf of the Operator and is the Operator's sub-processor under Art. 28(2) and (4) GDPR.

(C) Section 6.3 of the Customer DPA obliges the Operator to impose on each sub-processor, by contract, the same data protection obligations as the Customer DPA imposes on the Operator. This agreement does that.

(D) Routing to a Miner takes place only after this agreement has been concluded, the Miner has been verified (entity and Locations in the EU), the Operator has confirmed the Locations, Endpoints, hotkeys and sub-processors under sections 3.6 and 8.1, the notice period under section 6.2 of the Customer DPA (at least 30 days) has expired and any objections received have been dealt with, and the Operator has decided to route.

## 1. Subject matter, definitions, scope

1.1 This agreement governs the processing of personal data by the Miner on behalf of the Operator when the Miner answers requests that the Operator (or a system operated by the Operator) sends to the Endpoints named in Annex 4.

1.2 "Content" means everything the Miner receives in a request or produces for it: states, questions, options, images and other input, the results (responses), and all data derived from them, including tokens, embeddings, attention or prefix-cache values, intermediate values and partial results.

1.3 "EU" means the Member States of the European Union. "EU/EEA" means the Member States of the European Union and the other contracting states of the Agreement on the European Economic Area.

1.4 The subject matter, nature and purpose of the processing, the types of personal data and the categories of data subjects are set out in Annex 1. The Content is determined by the Operator's customers and may contain personal data.

1.5 This agreement applies to every request that reaches an Endpoint named in Annex 4 from the Operator, whatever tier the request is assigned to, so that the Miner does not need to distinguish tiers and the same protection applies to all Content.

1.6 This agreement does not govern the Miner's own business data (for example its customer, accounting and staff data) or the public data of the network protocol (for example the public hotkey and on-chain records). The Miner is responsible for these itself.

1.7 The Miner does not decide on the purposes and means of processing Content. If it nevertheless does so, it is considered a controller for that processing (Art. 28(10) GDPR) and infringes this agreement.

## 2. No routing commitment, no payment, protocol rewards

2.1 This agreement does not oblige the Operator to route any request or any volume of requests to the Miner. Routing is the Operator's decision alone. It takes place only after the steps named in Preamble (D). The Operator may restrict, suspend or stop routing at any time, without notice and without stating reasons, and without liability towards the Miner.

2.2 Except for cost reimbursement under section 11.3 and liability under section 14, the Operator owes the Miner no payment, fee, remuneration or compensation under this agreement. Whether and how the network's protocol rules take any of the Miner's answers into account, and whether any protocol rewards arise, is governed solely by those rules and not by this agreement. Protocol rewards are not consideration under this agreement; the Operator makes no statement, promise or guarantee about their existence, amount or value.

2.3 The Miner bears all its own costs, including hardware, hosting, energy, connectivity, staff and the costs of performing this agreement.

2.4 This agreement creates no partnership, agency, joint venture or employment relationship and no exclusivity for either party.

## 3. Requirements for the Miner, location, no transfer

3.1 The Miner confirms that it is a legal entity or partnership with legal capacity, established in the EU/EEA, acting in the course of its trade, business or profession, and that the person who accepts this agreement is authorised to represent it.

3.2 The Miner operates all hardware on which Content is processed (GPUs, CPUs, memory, storage, network equipment) exclusively in the data centres named in Annex 4, which are located in Member States of the European Union (the "Locations").

3.3 Content may not leave the European Union and may not be accessed from outside the European Union. This applies without exception to remote administration, support and maintenance access, monitoring, telemetry and crash reporting, backups, managed services, vendor or manufacturer support, and access by affiliated companies or staff who are physically outside the European Union, including staff who travel. Administrative access to systems that process Content is permitted only from devices and persons located in the European Union.

3.4 The Miner does not forward, proxy, relay, mirror or otherwise disclose Content to any third party or to any other location, except to its sub-processors under Annex 3. In particular, the Miner does not use third-party model APIs, rented or marketplace GPU capacity, or other compute that is not listed in Annex 3 and Annex 4, to answer requests.

3.5 The Miner gives the Operator accurate information on its entity, its Locations and its systems, and provides evidence on request (for example commercial register extract, VAT ID, data-centre contract or invoice, network or hardware information). The Operator may verify the information, including by non-intrusive technical checks of the Endpoints (for example network routing, latency, TLS configuration and responses to protocol requests); penetration tests or load tests require the Miner's prior consent in text form. The Miner does not use VPNs, tunnels, proxies or other techniques to disguise the actual location of the Endpoints or of the hardware.

3.6 The Miner notifies the Operator in text form of any change of entity data, Locations, Endpoints or hotkeys. A new or changed Location, Endpoint or hotkey is used for Content only after the Operator has confirmed it in text form and, for new locations and sub-processors, after the notice period in section 8.2.

## 4. Instructions

4.1 The Miner processes Content only on the documented instructions of the Operator, also with regard to transfers to third countries, unless it is required to do otherwise by Union or Member State law; in that case the Miner informs the Operator of that legal requirement before the processing, unless that law prohibits this on important grounds of public interest (Art. 28(3)(a) GDPR).

4.2 The Operator's documented instructions are this agreement including its annexes, the requests received at the Endpoints within the technical interface and the protocol of the network, and further instructions in text form to the Miner's contact in Annex 4.

4.3 The only permitted purpose is to compute the result of the request and return it to the sender. The Miner does not use Content for any other purpose, in particular not for training, fine-tuning, distillation, evaluation, benchmarking, profiling, analysis, product improvement, advertising, resale, publication, or the creation of data sets, and does not analyse or look at Content.

4.4 The Miner informs the Operator without undue delay if it believes that an instruction infringes the GDPR or other data protection provisions. It may suspend carrying out the instruction until the Operator confirms or changes it.

4.5 If an authority or a court requests access to Content or to systems that hold Content, the Miner informs the Operator without undue delay before any disclosure, unless prohibited by law, discloses nothing beyond what is legally compelled, and refers the authority to the Operator where possible.

4.6 The Operator ensures that it routes Content to the Miner only after completing the procedure under section 6.2 of the Customer DPA, informs the Miner without undue delay if a customer's objection or instruction requires the Miner to stop processing that customer's requests, and gives no instructions that it knows to infringe data protection law. The lawfulness of the Content sent is the responsibility of the Operator's customers as controllers and, in relation to the Miner, of the Operator; the Miner is not obliged to check it.

## 5. Confidentiality

The Miner ensures that all persons authorised to process Content, including those of its sub-processors, have committed themselves to confidentiality or are under an appropriate statutory obligation of confidentiality (Art. 28(3)(b) GDPR), that they process Content only on the Operator's instructions (Art. 29, Art. 32(4) GDPR), and that access is limited to what is strictly necessary for operating the systems. In normal operation no person looks at Content. The duty of confidentiality continues after the end of this agreement.

## 6. Zero retention of content

6.1 Content is held only in volatile working memory (system memory and GPU memory) for as long as the request is processed. It is not written to logs, databases, files, disks, swap space, core or crash dumps, queues, message brokers, caches, monitoring, tracing or error-reporting systems, backups, snapshots or any other persistent storage.

6.2 The Miner configures all components (inference server, runtime, reverse proxies, load balancers, firewalls, monitoring) so that no Content is logged. Debug, verbose and trace modes that record request or response bodies are disabled. Error messages and metrics contain no Content.

6.3 For performance, the inference server may keep intermediate values of recent requests in GPU memory (prefix cache) until they are overwritten by later requests, and at the latest until the server process restarts. This cache is never persisted, is isolated per model instance and cannot be read through the API. If the same inference process also answers requests from other network participants, the Miner ensures that cached values from the Operator's requests cannot be reused for, or detected through, requests of others — either by a separate inference instance for the Operator's requests or by cache separation per sender (for example a per-sender cache salt) — or disables prefix caching.

6.4 Swap space is disabled or encrypted with a key that is discarded at restart; core dumps and crash dumps that could contain memory are disabled.

6.5 The Miner does not copy, capture, mirror, tap or record Content, including by packet capture, TLS interception that stores payloads, or screenshots.

6.6 The Miner may process technical metadata without Content (for example request time, size, latency, status, error codes) for operation, security and the protocol. Metadata must not contain Content and is deleted after 14 days at the latest, unless a specific security incident requires individual entries to be kept longer to investigate it.

## 7. Technical and organisational measures

7.1 The Miner takes all measures required under Art. 32 GDPR. The measures that apply at least are set out in Annex 2, Part A. Part B contains the Miner's own description of its measures; it supplements Part A and does not reduce it. If Part B or any other entry of the Miner conflicts with this agreement or Part A, this agreement and Part A prevail.

7.2 The measures are subject to technical progress. The Miner may implement alternative adequate measures if the level of security is not reduced. Material changes are notified to the Operator in text form.

7.3 The Miner reviews the measures at least once a year and after every security incident, and documents the review.

## 8. Sub-processors of the Miner

8.1 The Operator gives the Miner general written authorisation to engage the sub-processors listed in Annex 3 (Art. 28(2) GDPR). Annex 3 contains in particular the operator of each data centre or colocation facility in which the Miner's hardware stands and any cloud or hosting provider, even if that provider has only physical access to the hardware. Ancillary services without any access to Content or to the systems that process it (for example electricity or network transit) are not sub-processing. The authorisation for the sub-processors entered by the Miner on acceptance, and the use of the Locations, Endpoints and hotkeys entered in Annex 4, take effect when the Operator confirms them in text form after verification. Until then no Content is routed to the Miner.

8.2 The Miner informs the Operator in text form of any intended addition or replacement of a sub-processor at least 45 days before the change takes effect, stating the name, address, service and location, and the safeguards. The Operator needs this period to inform its own customers 30 days in advance. The Operator may object on data protection grounds at any time before the change takes effect. If the Operator objects, the Miner does not use the new sub-processor for Content of the Operator; the Operator may in addition stop routing or terminate under section 15.

8.3 Sub-processors must be established in the EU/EEA, process Content only in the EU, and may not be accessible from outside the EU. In an urgent case, such as the sudden failure of a sub-processor, the Miner may replace it with a provider that meets the requirements of this section provided that it informs the Operator before using it; the Operator's objection right and its right to stop routing remain unaffected.

8.4 The Miner imposes on each sub-processor, by contract, the same data protection obligations as set out in this agreement, in particular sufficient guarantees for appropriate technical and organisational measures, the location requirement of section 8.3, the prohibition of retention and the audit and information rights (Art. 28(4) GDPR). It provides the Operator on request with the relevant parts of this contract.

8.5 The Miner remains fully liable to the Operator for the performance of its sub-processors' obligations.

## 9. Support with data subject rights

9.1 Taking into account the nature of the processing, the Miner assists the Operator by appropriate technical and organisational measures, insofar as possible, in responding to requests from data subjects under Chapter III GDPR (Art. 28(3)(e) GDPR). Because Content is not stored (section 6), there is normally no stored Content to access, correct or delete. On request the Miner confirms this in text form.

9.2 If a data subject or a third party contacts the Miner directly about Content, the Miner forwards the request to the Operator without undue delay, at the latest within two business days (Monday to Friday, excluding public holidays at the Miner's seat), and does not answer it itself unless instructed.

## 10. Support with Articles 32 to 36 GDPR; personal data breaches

10.1 The Miner assists the Operator in ensuring compliance with Articles 32 to 36 GDPR, taking into account the nature of the processing and the information available to it (Art. 28(3)(f) GDPR). This includes providing the information needed for a data protection impact assessment and prior consultation.

10.2 The Miner notifies the Operator at info@productivity-boost.com without undue delay, and at the latest within 24 hours, after becoming aware of a personal data breach affecting Content, or of an incident that gives reasonable grounds to suspect one. This includes unauthorised access to systems that process Content, compromise or loss of control of the hotkey or an Endpoint, discovery of Content in logs or storage, processing or access outside the EU, loss, theft or seizure of hardware, and breaches at a sub-processor.

10.3 The notification contains, as far as available: a description of the nature of the breach including the categories and approximate number of data subjects and records concerned; the name and contact details of a contact point; the likely consequences; and the measures taken or proposed to address the breach and mitigate its effects. Information that is not yet available is provided in phases without undue further delay.

10.4 The Miner takes the necessary measures to secure the systems and mitigate possible adverse consequences, and documents the breach. The Miner does not notify supervisory authorities, data subjects or third parties on behalf of the Operator or its customers unless the Operator instructs it to or the Miner is itself legally obliged to do so.

10.5 The Miner informs the Operator without undue delay of any other breach of this agreement, for example unintended retention of Content.

10.6 Each party bears its own costs of the support under sections 9 and 10.

## 11. Audits and information

11.1 The Miner makes available to the Operator all information necessary to demonstrate compliance with Art. 28 GDPR and allows for and contributes to audits, including inspections, conducted by the Operator or an auditor mandated by the Operator (Art. 28(3)(h) GDPR). This also serves the Operator in meeting audit rights of its own customers under section 10 of the Customer DPA.

11.2 The Miner may first provide current documentation: this agreement, the technical and organisational measures, the list of sub-processors, evidence of the Locations and, where available, certificates or audit reports of its sub-processors (for example ISO/IEC 27001 certificates of the data-centre operators). If this documentation is not sufficient to demonstrate compliance, the Operator may carry out inspections, including on site and remote inspections of system configuration. The Operator announces inspections with reasonable notice, normally 14 days, or without delay where there is a specific cause such as a personal data breach or an inquiry by a supervisory authority. Inspections take place during normal business hours and avoid unnecessary disruption of operations. Auditors must be bound to confidentiality; the Miner may object to an auditor who is its direct competitor, in which case the Operator appoints another auditor. Remote inspections are carried out by the Miner's staff presenting configuration and logs in a screen-sharing session or by providing exports; the Operator receives no independent access to production systems. On-site inspections in third-party data centres are subject to the access rules of the data-centre operator. Auditors may not access Content or data of the Miner's other customers.

11.3 Each party bears its own costs of inspections. The Miner may charge reasonable, proven costs for its support if the Operator conducts more than one inspection per calendar year without specific cause, unless an inspection reveals a material breach by the Miner.

11.4 The Miner cooperates with supervisory authorities on request (Art. 31 GDPR). Rights of supervisory authorities remain unaffected.

11.5 The Operator treats non-public information received from the Miner under sections 3.5, 8.4 and 11 as confidential, uses it only to verify and demonstrate compliance with this agreement and data protection law, and discloses it only to its auditors and legal advisers, to supervisory authorities, and — as far as necessary for section 10 of the Customer DPA — to customers bound to confidentiality. The Operator processes the personal data of the Miner's signatory and contacts as described in its privacy policy published on decisionmodels.io.

## 12. Deletion and return at the end of processing

12.1 Content is deleted as soon as the response has been returned, subject to section 6.3. No Content therefore remains to be returned or deleted at the end of this agreement. The Operator hereby chooses deletion; return is excluded because no Content is stored.

12.2 When this agreement ends, or earlier when routing stops and the Operator so requests, the Miner restarts the inference processes and clears the memory that held Content, and confirms in text form within 14 days that no Content remains.

12.3 If the Miner finds that Content was retained contrary to this agreement, it deletes it immediately, informs the Operator under section 10 and, on request, describes the extent and the cause.

12.4 Statutory retention obligations apply only to the Miner's own business data and never justify keeping Content.

## 13. Records and contact

The Miner keeps the records required by Art. 30(2) GDPR and names in Annex 4 a contact for data protection (and a data protection officer, where one is required by law). The Operator's contact is info@productivity-boost.com.

## 14. Liability

14.1 Liability towards data subjects is governed by Art. 82 GDPR. Between the parties, Art. 82(5) GDPR and the statutory provisions on recourse apply.

14.2 The Miner is liable to the Operator under the statutory provisions for breaches of this agreement by itself and its sub-processors, subject to section 14.3. Insofar as the Miner is responsible for a breach of this agreement or of data protection law (by itself or its sub-processors), it indemnifies the Operator against claims of third parties (in particular customers and data subjects) and against reasonable costs of legal defence. Administrative fines imposed on the Operator are covered only insofar as they are attributable to the Miner's breach and recourse is legally permissible. The Operator informs the Miner without undue delay of such claims, allows it to take part in the defence, and does not acknowledge or settle them without the Miner's consent, which may not be unreasonably withheld. § 254 BGB (contributory fault) applies.

14.3 Each party is liable without limitation for intent and gross negligence, for injury to life, body or health, under the Product Liability Act, for guarantees given, and where mandatory law so requires. Otherwise, for slight negligence, a party is liable only for breach of an essential contractual obligation (an obligation the fulfilment of which makes the proper performance of the agreement possible in the first place and on which the other party may regularly rely), limited to the foreseeable damage typical for this kind of agreement and to EUR 50,000 per calendar year. For the Miner, the obligations in sections 3.3, 3.4, 4.3 and 6 are essential contractual obligations. Liability towards data subjects under Art. 82 GDPR remains unaffected. Section 2 remains unaffected: because the agreement gives no claim to routing or to rewards, the Operator owes no compensation for rewards or expected benefits that are not earned because routing is restricted, suspended or stopped.

## 15. Term and termination

15.1 This agreement takes effect on acceptance (date in the record of conclusion) and runs for an indefinite period.

15.2 Either party may terminate this agreement in text form with 14 days' notice.

15.3 The Operator may stop routing at any time under section 2.1. Stopping routing does not end this agreement unless the Operator declares termination; the Miner's obligations continue as long as Content is in its systems.

15.4 Each party may terminate for good cause with immediate effect (§ 314 BGB). Good cause for the Operator exists in particular if the Miner breaches sections 3, 4, 6 or 10, has made incorrect statements on its entity or Locations, loses control of the hotkey or the Endpoints, or if continued routing to the Miner would infringe a statutory obligation or an order of an authority.

15.5 After the end of this agreement section 12 applies. Sections 5, 10, 11 (for twelve months after the end), 12, 14 and 17 and the Miner's obligations from section 4 for Content still in its possession continue to apply.

## 16. Changes

16.1 The Operator may change this agreement where this is necessary for legal or regulatory reasons, because of changes to the Customer DPA, or to adapt the technical and organisational measures to the state of the art, by announcing the new version in text form at least 45 days in advance, highlighting the changes. Changes that extend the Miner's liability, introduce payment obligations of the Miner or restrict its termination rights require the Miner's express consent. For other changes, the Miner may object in text form within 30 days of receipt; without an objection within this period the new version applies from the stated date; the announcement points this out.

16.2 If the Miner objects, the previous version continues to apply. Either party may then terminate with 14 days' notice; where the change is legally necessary, the Operator may instead stop routing with immediate effect.

16.3 Changes to Locations, Endpoints, hotkeys and sub-processors follow sections 3.6 and 8; the Operator's agreement to an updated Annex 4 is given in text form.

## 17. Final provisions

17.1 This agreement is concluded in the electronic form described in the record of conclusion above. Notices under this agreement are given in text form to the contacts in Annex 4; for the Operator to info@productivity-boost.com.

17.2 As regards the processing of Content, this agreement takes precedence over other terms of the parties and over any terms of the Miner. The protocol rules of the network govern only the relationship of the Miner to the network and do not override this agreement.

17.3 Neither party may assign rights or transfer obligations under this agreement without the other party's prior consent in text form, which may not be unreasonably withheld; § 354a HGB remains unaffected.

17.4 German law applies, excluding the UN Convention on Contracts for the International Sale of Goods and the conflict-of-law rules. The place of jurisdiction for disputes arising from or in connection with this agreement is Passau, if the Miner is a merchant, a legal person under public law or a special fund under public law, and, as far as permitted, also for Miners established in another Member State. The Operator may also sue at the Miner's seat.

17.5 This agreement exists in English and in German. If the two versions differ, the German version prevails.

17.6 If a provision of this agreement is invalid, the rest remains valid. The invalid provision is replaced by the valid provision that comes closest to its purpose.

## Annex 1 — Details of the processing

1. **Subject matter and purpose:** typed-decision inference. The Operator (for its customers) sends a state (text and, where supported, images), a question and answer options to the Miner's Endpoint; the model operated by the Miner computes probabilities for the answer options and returns them to the Operator. The purpose is solely to provide this result.

2. **Nature of processing:** receipt over an encrypted connection, temporary storage in the working memory of the Miner's inference servers (system memory and GPU memory), computation by the model, return of the result, deletion. No storage of Content.

3. **Types of personal data:** determined by the customers of the Operator. Typically any personal data contained in the texts or images submitted, for example names, contact details, contents of messages, tickets, documents or transactions, descriptions of behaviour or preferences, and images that may show people. Special categories of personal data (Art. 9 GDPR) only to the extent the customer has a legal basis and has assessed the measures as appropriate.

4. **Categories of data subjects:** determined by the customers of the Operator. Typically their customers, users, prospects, employees, contractors and business partners and other people mentioned in the submitted content.

5. **Retention of Content:** none (zero retention). Content and results are not written to logs, databases, disk or any other persistent storage. They are held in volatile working memory while the request is processed. For performance, the inference server may keep intermediate values of recent requests in GPU memory (prefix cache) until they are overwritten by later requests, and at the latest until the server process restarts; this cache is never persisted, is isolated as described in section 6.3 and cannot be read through the API. Metadata without Content: section 6.6.

6. **Place of processing:** exclusively the Locations named in Annex 4, in Member States of the European Union; no access from outside the EU.

7. **Duration:** for the term of this agreement and until deletion under section 12.

8. **Contact for data protection at the Operator:** info@productivity-boost.com.

## Annex 2 — Technical and organisational measures (Art. 32 GDPR)

### Part A — Minimum measures the Miner commits to

**A.1 Encryption (Art. 32(1)(a))**

- All Endpoints are reachable only over TLS 1.2 or higher; plain HTTP is refused.
- Connections between components that handle Content (proxy, inference server, tunnels) are encrypted and authenticated.
- All disks and volumes of systems that process Content use full-disk encryption; keys are not stored on the same disk.

**A.2 Confidentiality (Art. 32(1)(b))**

- Physical access: the hardware stands in the data centres named in Annex 4, in locked racks or cages with access control and logging by the data-centre operator.
- System access: administrative access only through SSH with public keys or a console with multi-factor authentication (MFA); no password logins; firewalls allow only the required ports.
- Admin access only from the EU: administrative access to systems that process Content comes only from devices and persons located in the EU.
- Access control: named administrators, need-to-know, role-based, access reviewed at least once a year; no shared accounts.
- Isolation of the inference process: the inference process runs under its own unprivileged user or in its own container or virtual machine, with no shared file systems with other workloads; no workloads of third parties (including other customers of the Miner) on the same GPU; other workloads on the same host only in separate virtual machines or containers without access to the memory, GPU or network paths of the inference process; the inference process has only the network paths it needs. Answering requests of other network participants under the protocol through the same inference process is permitted subject to section 6.3.
- No Content in development or test systems.
- No content logs: logs contain only IDs, sizes, latency, model and status, never request or response content; debug and trace modes that record bodies are disabled; no content in monitoring, tracing or crash reports.

**A.3 Integrity (Art. 32(1)(b))**

- Transfer control: encryption in transit (A.1); no removable media for Content.
- Input control: administrative actions and changes to the configuration are logged.
- Model weights and container images are those required by the network protocol and are verified by checksum; the Miner does not alter results.

**A.4 Availability and resilience (Art. 32(1)(b) and (c))**

- Monitoring of the services with automatic restart of failed processes.
- Patching: security updates for operating system, GPU driver, inference software and exposed services are applied without undue delay; critical updates at the latest within 7 days of release, other security updates within 30 days.
- Backups, if any, contain only configuration, never Content.

**A.5 Key protection**

- The hotkey and any other signing or authentication keys are stored encrypted or in a protected key store with access limited to named persons, are not placed in source code or logs, and are not shared with third parties.
- Loss, suspected compromise or unauthorised use of a key is reported under section 10.2 and the key is rotated without undue delay.

**A.6 Regular testing and evaluation (Art. 32(1)(d))**

- Vulnerability scanning of exposed systems and review of these measures at least once a year and after every security incident.
- Documented incident process: detection, containment, assessment, notification of the Operator within 24 hours (section 10.2), follow-up.

**A.7 Organisational measures**

- Everyone with access is bound to confidentiality and instructed in data protection.
- Art. 28 GDPR agreements with sub-processors are concluded before they gain access (section 8.4).
- Administrator devices use full-disk encryption, screen lock and current security updates.
- Secrets are kept in protected stores, never in source code or logs.

### Part B — Miner's own description of its measures

{{tom_statement}}

## Annex 3 — Sub-processors of the Miner

| Sub-processor (name, address) | Service | Location of processing | Safeguard |
| --- | --- | --- | --- |
{{own_subprocessors}}

Changes only under section 8.

## Annex 4 — Contacts, Locations and Endpoints

| Item | Value |
| --- | --- |
| Data protection contact of the Miner | {{privacy_contact}} |
| Authorised signatory | {{signatory_name}}, {{signatory_role}}, {{signatory_email}} |
| Locations (data centres in the EU) | {{dc_locations}} |
| Hotkeys (SS58) | {{hotkeys}} |
| Endpoints | {{endpoints}} |
| Operator contact | info@productivity-boost.com |
