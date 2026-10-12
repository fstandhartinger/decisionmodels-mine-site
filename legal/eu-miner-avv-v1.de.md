# Vertrag über die Unterauftragsverarbeitung für EU-Miner (Art. 28 Abs. 2 und 4 DSGVO)

Decision Models — REAX-Netzwerk (Bittensor-Subnet 92)

Version {{version}} · Vertrags-ID {{agreement_id}}

*ENTWURFSTEXT für das dauerhafte Angebot auf mine.decisionmodels.io. Weichen die Sprachfassungen voneinander ab, geht die deutsche Fassung vor (Abschnitt 17.5).*

## Parteien

**Betreiber („Betreiber“, „Auftragsverarbeiter“ oder „wir“)**

productivity-boost.com Betriebs UG (haftungsbeschränkt) & Co. KG, Reichenberger Str. 2, 94036 Passau, Deutschland, Amtsgericht Passau HRA 12725, vertreten durch ihre persönlich haftende Gesellschafterin productivity-boost.com UG (haftungsbeschränkt) (Amtsgericht Passau HRB 8453), diese vertreten durch ihren Geschäftsführer Florian Standhartinger. Marke: Decision Models (decisionmodels.io). Kontakt für diesen Vertrag: info@productivity-boost.com.

**Miner („Miner“ oder „Unterauftragsverarbeiter“)**

{{miner_company}} ({{miner_legal_form}}), {{miner_address}}, {{miner_country}}, Handelsregister: {{miner_register}}, USt-IdNr.: {{miner_vat_id}}, vertreten durch {{signatory_name}} ({{signatory_role}}), E-Mail {{signatory_email}}.

Datenschutzkontakt des Miners: {{privacy_contact}}.

## Abschlussprotokoll

| Angabe | Wert |
| --- | --- |
| Vertrags-ID | {{agreement_id}} |
| Version des Textes | {{version}} |
| Angenommen am (UTC) | {{accepted_at}} |
| SHA-256 des Textes dieser Version in der veröffentlichten Fassung | {{text_sha256}} |

Die Erklärung des Betreibers ist ein auf mine.decisionmodels.io veröffentlichtes, dauerhaftes Angebot, das der Betreiber seinerseits für jeden Miner, der die Verifizierung durchläuft, bereits angenommen hat. Der Miner nimmt durch elektronische Erklärung eines vertretungsberechtigten Unterzeichners an (Name, Funktion, Unternehmen, E-Mail-Adresse und Bestätigung „Ich bin berechtigt, das oben genannte Unternehmen zu vertreten“). Die Annahme wird mit Zeitstempel, IP-Adresse, Version und dem SHA-256-Hash des genauen Textes protokolliert. Diese Textform genügt Art. 28 Abs. 9 DSGVO. Der Miner kann eine Kopie als PDF anfordern.

## Präambel

(A) Der Betreiber erbringt den Inferenzdienst Decision Models (Inferenz für typisierte Entscheidungen: ein Zustand, eine Frage und Antwortoptionen gehen hinein, Wahrscheinlichkeiten kommen heraus). Für seine API-Kunden handelt der Betreiber als Auftragsverarbeiter auf Grundlage seines Auftragsverarbeitungsvertrags (Version 1.2 oder neuer, „Kunden-AVV“).

(B) Der Betreiber kann künftig Anfragen seines EU-Tarifs an unabhängige Unternehmen weiterleiten, die GPU-Hardware in Rechenzentren in der EU/im EWR betreiben und als Miner am REAX-Netzwerk (Bittensor-Subnet 92) teilnehmen. Ein Miner, der solche Anfragen erhält, verarbeitet personenbezogene Daten im Auftrag des Betreibers und ist dessen Unterauftragsverarbeiter nach Art. 28 Abs. 2 und 4 DSGVO.

(C) Nach Abschnitt 6.3 des Kunden-AVV muss der Betreiber jedem Unterauftragsverarbeiter vertraglich dieselben Datenschutzpflichten auferlegen, die der Kunden-AVV dem Betreiber auferlegt. Dieser Vertrag tut das.

(D) Eine Weiterleitung an einen Miner erfolgt erst, nachdem dieser Vertrag geschlossen wurde, der Miner verifiziert wurde (Unternehmen und Standort in der EU/im EWR), die Kunden des Betreibers die 30-tägige Mitteilung nach Abschnitt 6.2 des Kunden-AVV erhalten haben und der Betreiber sich für die Weiterleitung entschieden hat.

## 1. Gegenstand, Begriffe, Geltungsbereich

1.1 Dieser Vertrag regelt die Verarbeitung personenbezogener Daten durch den Miner im Auftrag des Betreibers, wenn der Miner Anfragen beantwortet, die der Betreiber (oder ein vom Betreiber betriebenes System) an die in Anlage 4 genannten Endpunkte sendet.

1.2 „Inhalte“ ist alles, was der Miner in einer Anfrage erhält oder für sie erzeugt: Zustände, Fragen, Optionen, Bilder und sonstige Eingaben, die Ergebnisse (Antworten) und alle daraus abgeleiteten Daten, einschließlich Token, Embeddings, Attention- oder Prefix-Cache-Werte, Zwischenwerte und Teilergebnisse.

1.3 „EU/EWR“ sind die Mitgliedstaaten der Europäischen Union und die übrigen Vertragsstaaten des Abkommens über den Europäischen Wirtschaftsraum.

1.4 Gegenstand, Art und Zweck der Verarbeitung, die Arten personenbezogener Daten und die Kategorien betroffener Personen ergeben sich aus Anlage 1. Die Inhalte werden von den Kunden des Betreibers bestimmt und können personenbezogene Daten enthalten.

1.5 Dieser Vertrag gilt für jede Anfrage, die vom Betreiber an einem in Anlage 4 genannten Endpunkt eingeht, gleich welchem Tarif die Anfrage zugeordnet ist, damit der Miner Tarife nicht unterscheiden muss und für alle Inhalte derselbe Schutz gilt.

1.6 Dieser Vertrag regelt nicht die eigenen Geschäftsdaten des Miners (zum Beispiel Kunden-, Buchhaltungs- und Personaldaten) und nicht die öffentlichen Daten des Netzwerkprotokolls (zum Beispiel den öffentlichen Hotkey und Einträge auf der Blockchain). Dafür ist der Miner selbst verantwortlich.

1.7 Der Miner entscheidet nicht über die Zwecke und Mittel der Verarbeitung von Inhalten. Tut er es dennoch, gilt er für diese Verarbeitung als Verantwortlicher (Art. 28 Abs. 10 DSGVO) und verstößt gegen diesen Vertrag.

## 2. Keine Zusage zur Weiterleitung, keine Zahlung, Protokollbelohnungen

2.1 Dieser Vertrag verpflichtet den Betreiber nicht, Anfragen oder ein bestimmtes Volumen an Anfragen an den Miner weiterzuleiten. Die Weiterleitung ist allein Entscheidung des Betreibers. Sie erfolgt erst nach den in Präambel (D) genannten Schritten. Der Betreiber kann die Weiterleitung jederzeit ohne Vorankündigung und ohne Angabe von Gründen einschränken, aussetzen oder beenden, ohne dem Miner gegenüber zu haften.

2.2 Der Betreiber schuldet dem Miner aus diesem Vertrag keine Zahlung, Gebühr, Vergütung oder Entschädigung. Belohnungen, falls es welche gibt, entstehen ausschließlich nach den Protokollregeln des Netzwerks. Sie sind keine Gegenleistung aus diesem Vertrag; der Betreiber sagt sie und ihre Höhe weder zu noch garantiert er sie und ist nicht verpflichtet, sie zu beeinflussen.

2.3 Der Miner trägt alle eigenen Kosten, einschließlich Hardware, Hosting, Energie, Anbindung, Personal und der Kosten der Vertragserfüllung.

2.4 Dieser Vertrag begründet keine Gesellschaft, Vertretung, Partnerschaft oder Beschäftigung und keine Exklusivität für eine der Parteien.

## 3. Anforderungen an den Miner, Standort, keine Übermittlung

3.1 Der Miner bestätigt, dass er eine rechtsfähige juristische Person oder Personengesellschaft mit Sitz in der EU/im EWR ist, die im Rahmen ihrer gewerblichen oder beruflichen Tätigkeit handelt, und dass die Person, die diesen Vertrag annimmt, zu seiner Vertretung berechtigt ist.

3.2 Der Miner betreibt sämtliche Hardware, auf der Inhalte verarbeitet werden (GPUs, CPUs, Arbeitsspeicher, Speicher, Netzwerktechnik), ausschließlich in den in Anlage 4 genannten Rechenzentren in der EU/im EWR (die „Standorte“).

3.3 Inhalte dürfen die EU/den EWR nicht verlassen und dürfen nicht von außerhalb der EU/des EWR eingesehen oder abgerufen werden. Das gilt ausnahmslos für Fernadministration, Support- und Wartungszugriffe, Monitoring, Telemetrie und Absturzberichte, Backups, Managed Services, Hersteller- oder Lieferantensupport sowie für Zugriffe verbundener Unternehmen oder von Personal, das sich physisch außerhalb der EU/des EWR befindet, auch auf Reisen. Administrativer Zugriff auf Systeme, die Inhalte verarbeiten, ist nur von Geräten und Personen zulässig, die sich in der EU/im EWR befinden.

3.4 Der Miner leitet Inhalte nicht an Dritte oder andere Orte weiter, spiegelt oder offenbart sie nicht und setzt keine Proxys oder Relays dafür ein, außer gegenüber seinen Unterauftragsverarbeitern nach Anlage 3. Insbesondere nutzt der Miner zur Beantwortung von Anfragen keine Modell-APIs Dritter, keine gemietete oder über Marktplätze vermittelte GPU-Kapazität und keine sonstige Rechenleistung, die nicht in Anlage 3 und Anlage 4 aufgeführt ist.

3.5 Der Miner gibt dem Betreiber zutreffende Auskunft über sein Unternehmen, seine Standorte und seine Systeme und legt auf Verlangen Nachweise vor (zum Beispiel Handelsregisterauszug, USt-IdNr., Rechenzentrumsvertrag oder -rechnung, Netzwerk- oder Hardwareangaben). Der Betreiber darf die Angaben prüfen, auch durch technische Prüfungen der Endpunkte. Der Miner setzt keine VPNs, Tunnel, Proxys oder andere Techniken ein, die den tatsächlichen Standort der Endpunkte oder der Hardware verschleiern.

3.6 Der Miner teilt dem Betreiber jede Änderung seiner Unternehmensangaben, Standorte, Endpunkte oder Hotkeys in Textform mit. Ein neuer oder geänderter Standort, Endpunkt oder Hotkey wird für Inhalte erst verwendet, nachdem der Betreiber ihn in Textform bestätigt hat, und bei neuen Standorten und Unterauftragsverarbeitern erst nach Ablauf der Frist nach Abschnitt 8.2.

## 4. Weisungen

4.1 Der Miner verarbeitet Inhalte nur auf dokumentierte Weisung des Betreibers, auch in Bezug auf Übermittlungen in Drittländer, außer er ist nach Unionsrecht oder dem Recht eines Mitgliedstaats zu anderer Verarbeitung verpflichtet; in diesem Fall teilt der Miner dem Betreiber diese rechtlichen Anforderungen vor der Verarbeitung mit, sofern das betreffende Recht dies nicht wegen eines wichtigen öffentlichen Interesses verbietet (Art. 28 Abs. 3 lit. a DSGVO).

4.2 Die dokumentierten Weisungen des Betreibers sind dieser Vertrag einschließlich seiner Anlagen, die an den Endpunkten im Rahmen der technischen Schnittstelle und des Protokolls des Netzwerks eingehenden Anfragen sowie weitere Weisungen in Textform an den Kontakt des Miners nach Anlage 4.

4.3 Einziger zulässiger Zweck ist, das Ergebnis der Anfrage zu berechnen und an den Absender zurückzugeben. Der Miner nutzt Inhalte nicht zu anderen Zwecken, insbesondere nicht für Training, Fine-Tuning, Distillation, Evaluierung, Benchmarking, Profilbildung, Analyse, Produktverbesserung, Werbung, Weiterverkauf, Veröffentlichung oder die Erstellung von Datensätzen, und wertet Inhalte nicht aus und sieht sie nicht ein.

4.4 Der Miner informiert den Betreiber unverzüglich, wenn er der Auffassung ist, dass eine Weisung gegen die DSGVO oder andere Datenschutzvorschriften verstößt. Er darf die Ausführung der Weisung aussetzen, bis der Betreiber sie bestätigt oder ändert.

4.5 Verlangt eine Behörde oder ein Gericht Zugang zu Inhalten oder zu Systemen, die Inhalte enthalten, informiert der Miner den Betreiber vor jeder Offenlegung unverzüglich, sofern das Gesetz dies nicht verbietet, legt nicht mehr offen, als rechtlich zwingend ist, und verweist die Behörde nach Möglichkeit an den Betreiber.

## 5. Vertraulichkeit

Der Miner stellt sicher, dass alle Personen, die zur Verarbeitung von Inhalten befugt sind, auch die seiner Unterauftragsverarbeiter, sich zur Vertraulichkeit verpflichtet haben oder einer angemessenen gesetzlichen Verschwiegenheitspflicht unterliegen (Art. 28 Abs. 3 lit. b DSGVO), dass sie Inhalte nur auf Weisung des Betreibers verarbeiten (Art. 29, Art. 32 Abs. 4 DSGVO) und dass der Zugriff auf das für den Betrieb der Systeme unbedingt Erforderliche beschränkt ist. Im Normalbetrieb sieht niemand Inhalte ein. Die Vertraulichkeitspflicht besteht nach Beendigung dieses Vertrags fort.

## 6. Keine Speicherung von Inhalten

6.1 Inhalte werden nur im flüchtigen Arbeitsspeicher (System- und GPU-Speicher) gehalten, solange die Anfrage verarbeitet wird. Sie werden nicht in Logs, Datenbanken, Dateien, Datenträger, Swap-Speicher, Core- oder Absturz-Dumps, Warteschlangen, Message-Broker, Caches, Monitoring-, Tracing- oder Fehlerberichtssysteme, Backups, Snapshots oder sonstigen dauerhaften Speicher geschrieben.

6.2 Der Miner konfiguriert alle Komponenten (Inferenzserver, Laufzeitumgebung, Reverse-Proxys, Load Balancer, Firewalls, Monitoring) so, dass keine Inhalte protokolliert werden. Debug-, Verbose- und Trace-Modi, die Anfrage- oder Antwortkörper aufzeichnen, sind deaktiviert. Fehlermeldungen und Metriken enthalten keine Inhalte.

6.3 Zur Leistungssteigerung darf der Inferenzserver Zwischenwerte aktueller Anfragen im GPU-Speicher vorhalten (Prefix-Cache), bis sie von späteren Anfragen überschrieben werden, spätestens bis zum Neustart des Serverprozesses. Dieser Cache wird nie persistiert, ist je Modellinstanz isoliert und kann über die API nicht ausgelesen werden.

6.4 Swap-Speicher ist deaktiviert oder mit einem Schlüssel verschlüsselt, der beim Neustart verworfen wird; Core- und Absturz-Dumps, die Speicherinhalte enthalten könnten, sind deaktiviert.

6.5 Der Miner kopiert, erfasst, spiegelt, greift ab oder zeichnet Inhalte nicht auf, auch nicht durch Paketmitschnitte, TLS-Interception mit Speicherung der Nutzdaten oder Screenshots.

6.6 Der Miner darf technische Metadaten ohne Inhalte (zum Beispiel Zeitpunkt, Größe, Latenz, Status, Fehlercodes) für Betrieb, Sicherheit und das Protokoll verarbeiten. Metadaten dürfen keine Inhalte enthalten und werden spätestens nach 14 Tagen gelöscht, außer ein konkreter Sicherheitsvorfall erfordert, einzelne Einträge zur Aufklärung länger aufzubewahren.

## 7. Technische und organisatorische Maßnahmen

7.1 Der Miner trifft alle nach Art. 32 DSGVO erforderlichen Maßnahmen. Die mindestens geltenden Maßnahmen ergeben sich aus Anlage 2 Teil A. Teil B enthält die eigene Beschreibung der Maßnahmen durch den Miner; sie ergänzt Teil A und mindert ihn nicht.

7.2 Die Maßnahmen unterliegen dem technischen Fortschritt. Der Miner darf alternative angemessene Maßnahmen umsetzen, wenn das Sicherheitsniveau nicht sinkt. Wesentliche Änderungen teilt er dem Betreiber in Textform mit.

7.3 Der Miner überprüft die Maßnahmen mindestens einmal jährlich und nach jedem Sicherheitsvorfall und dokumentiert die Überprüfung.

## 8. Unterauftragsverarbeiter des Miners

8.1 Der Betreiber erteilt dem Miner die allgemeine schriftliche Genehmigung, die in Anlage 3 aufgeführten Unterauftragsverarbeiter einzusetzen (Art. 28 Abs. 2 DSGVO). Anlage 3 enthält insbesondere den Betreiber jedes Rechenzentrums oder jeder Colocation-Einrichtung, in der die Hardware des Miners steht, und jeden Cloud- oder Hosting-Anbieter, auch wenn dieser nur physischen Zugang zur Hardware hat. Nebenleistungen ohne jeden Zugang zu Inhalten oder zu den Systemen, die sie verarbeiten (zum Beispiel Strom oder Netzwerk-Transit), sind keine Unterauftragsverarbeitung.

8.2 Der Miner informiert den Betreiber in Textform über jede beabsichtigte Hinzuziehung oder Ersetzung eines Unterauftragsverarbeiters mindestens 45 Tage, bevor die Änderung wirksam wird, unter Angabe von Name, Anschrift, Leistung, Standort und Garantien. Der Betreiber benötigt diese Frist, um seine Kunden 30 Tage im Voraus zu informieren. Der Betreiber kann jederzeit, bevor die Änderung wirksam wird, aus Datenschutzgründen widersprechen. Widerspricht der Betreiber, setzt der Miner den neuen Unterauftragsverarbeiter nicht für Inhalte des Betreibers ein; der Betreiber kann zusätzlich die Weiterleitung beenden oder nach Abschnitt 15 kündigen.

8.3 Unterauftragsverarbeiter müssen ihren Sitz in der EU/im EWR haben, Inhalte nur in der EU/im EWR verarbeiten und dürfen nicht von außerhalb der EU/des EWR zugänglich sein. In dringenden Fällen, etwa beim plötzlichen Ausfall eines Unterauftragsverarbeiters, darf der Miner ihn durch einen Anbieter ersetzen, der die Anforderungen dieses Abschnitts erfüllt, nur wenn er den Betreiber vor dem Einsatz informiert; das Widerspruchsrecht des Betreibers und sein Recht, die Weiterleitung zu beenden, bleiben unberührt.

8.4 Der Miner erlegt jedem Unterauftragsverarbeiter vertraglich dieselben Datenschutzpflichten auf, die in diesem Vertrag festgelegt sind, insbesondere hinreichende Garantien für geeignete technische und organisatorische Maßnahmen, die Standortanforderung EU/EWR, das Speicherverbot sowie die Prüf- und Auskunftsrechte (Art. 28 Abs. 4 DSGVO). Er legt dem Betreiber auf Verlangen die maßgeblichen Teile dieses Vertrags vor.

8.5 Der Miner haftet gegenüber dem Betreiber in vollem Umfang dafür, dass seine Unterauftragsverarbeiter ihre Pflichten erfüllen.

## 9. Unterstützung bei Betroffenenrechten

9.1 Unter Berücksichtigung der Art der Verarbeitung unterstützt der Miner den Betreiber mit geeigneten technischen und organisatorischen Maßnahmen, soweit möglich, bei der Beantwortung von Anträgen betroffener Personen nach Kapitel III DSGVO (Art. 28 Abs. 3 lit. e DSGVO). Weil Inhalte nicht gespeichert werden (Abschnitt 6), gibt es normalerweise keine gespeicherten Inhalte, die auszukunften, zu berichtigen oder zu löschen wären. Der Miner bestätigt dies auf Verlangen in Textform.

9.2 Wendet sich eine betroffene Person oder ein Dritter wegen Inhalten unmittelbar an den Miner, leitet er die Anfrage unverzüglich, spätestens innerhalb von zwei Werktagen, an den Betreiber weiter und beantwortet sie nicht selbst, außer er ist dazu angewiesen.

## 10. Unterstützung nach Art. 32 bis 36 DSGVO; Verletzungen des Schutzes personenbezogener Daten

10.1 Der Miner unterstützt den Betreiber bei der Einhaltung der Art. 32 bis 36 DSGVO unter Berücksichtigung der Art der Verarbeitung und der ihm zur Verfügung stehenden Informationen (Art. 28 Abs. 3 lit. f DSGVO). Dazu gehört, die für eine Datenschutz-Folgenabschätzung und eine vorherige Konsultation erforderlichen Informationen bereitzustellen.

10.2 Der Miner meldet dem Betreiber an info@productivity-boost.com unverzüglich, spätestens innerhalb von 24 Stunden, nachdem ihm eine Verletzung des Schutzes personenbezogener Daten bekannt wurde, die Inhalte betrifft, oder ein Vorfall, der den begründeten Verdacht einer solchen Verletzung ergibt. Dazu zählen unbefugter Zugriff auf Systeme, die Inhalte verarbeiten, Kompromittierung oder Kontrollverlust über den Hotkey oder einen Endpunkt, das Auffinden von Inhalten in Logs oder Speichern, Verarbeitung oder Zugriff außerhalb der EU/des EWR, Verlust, Diebstahl oder Beschlagnahme von Hardware sowie Verletzungen bei einem Unterauftragsverarbeiter.

10.3 Die Meldung enthält, soweit verfügbar: eine Beschreibung der Art der Verletzung einschließlich der Kategorien und der ungefähren Zahl der betroffenen Personen und Datensätze; Name und Kontaktdaten einer Anlaufstelle; die wahrscheinlichen Folgen; und die ergriffenen oder vorgeschlagenen Maßnahmen zur Behebung und zur Abmilderung der Folgen. Noch nicht verfügbare Informationen werden schrittweise ohne unangemessene weitere Verzögerung nachgereicht.

10.4 Der Miner trifft die erforderlichen Maßnahmen zur Sicherung der Systeme und zur Minderung möglicher nachteiliger Folgen und dokumentiert die Verletzung. Der Miner meldet nicht im Namen des Betreibers oder seiner Kunden an Aufsichtsbehörden, betroffene Personen oder Dritte, außer der Betreiber weist ihn dazu an oder der Miner ist selbst gesetzlich dazu verpflichtet.

10.5 Der Miner informiert den Betreiber unverzüglich über jeden sonstigen Verstoß gegen diesen Vertrag, zum Beispiel unbeabsichtigte Speicherung von Inhalten.

10.6 Jede Partei trägt die eigenen Kosten der Unterstützung nach den Abschnitten 9 und 10.

## 11. Prüfungen und Auskünfte

11.1 Der Miner stellt dem Betreiber alle erforderlichen Informationen zum Nachweis der Einhaltung von Art. 28 DSGVO zur Verfügung und ermöglicht Überprüfungen, einschließlich Inspektionen, die vom Betreiber oder einem vom Betreiber beauftragten Prüfer durchgeführt werden, und trägt dazu bei (Art. 28 Abs. 3 lit. h DSGVO). Das dient auch dem Betreiber dazu, Prüfrechte seiner eigenen Kunden nach Abschnitt 10 des Kunden-AVV zu erfüllen.

11.2 Der Miner darf zunächst aktuelle Unterlagen vorlegen: diesen Vertrag, die technischen und organisatorischen Maßnahmen, die Liste der Unterauftragsverarbeiter, Nachweise über die Standorte und, soweit verfügbar, Zertifikate oder Prüfberichte seiner Unterauftragsverarbeiter (zum Beispiel ISO/IEC-27001-Zertifikate der Rechenzentrumsbetreiber). Reichen diese Unterlagen zum Nachweis der Einhaltung nicht aus, darf der Betreiber Inspektionen durchführen, auch vor Ort sowie als Fernprüfung der Systemkonfiguration. Der Betreiber kündigt Inspektionen mit angemessener Frist an, in der Regel 14 Tage, oder unverzüglich, wenn ein besonderer Anlass vorliegt, etwa eine Verletzung des Schutzes personenbezogener Daten oder eine Anfrage einer Aufsichtsbehörde. Inspektionen finden während der üblichen Geschäftszeiten statt und vermeiden unnötige Störungen des Betriebs. Prüfer müssen zur Vertraulichkeit verpflichtet sein; der Miner darf einem Prüfer widersprechen, der sein direkter Wettbewerber ist, woraufhin der Betreiber einen anderen Prüfer benennt.

11.3 Jede Partei trägt die eigenen Kosten von Inspektionen. Der Miner darf angemessene, nachgewiesene Kosten seiner Unterstützung berechnen, wenn der Betreiber ohne besonderen Anlass mehr als eine Inspektion pro Kalenderjahr durchführt, es sei denn, eine Inspektion deckt einen wesentlichen Verstoß des Miners auf.

11.4 Der Miner arbeitet auf Anfrage mit Aufsichtsbehörden zusammen (Art. 31 DSGVO). Rechte der Aufsichtsbehörden bleiben unberührt.

## 12. Löschung und Rückgabe nach Ende der Verarbeitung

12.1 Inhalte werden gelöscht, sobald die Antwort zurückgegeben wurde, vorbehaltlich Abschnitt 6.3. Bei Vertragsende bleiben daher keine Inhalte zurückzugeben oder zu löschen.

12.2 Bei Beendigung dieses Vertrags oder früher, wenn die Weiterleitung beendet ist und der Betreiber dies verlangt, startet der Miner die Inferenzprozesse neu, leert den Speicher, der Inhalte gehalten hat, und bestätigt innerhalb von 14 Tagen in Textform, dass keine Inhalte verblieben sind.

12.3 Stellt der Miner fest, dass Inhalte entgegen diesem Vertrag gespeichert wurden, löscht er sie unverzüglich, informiert den Betreiber nach Abschnitt 10 und beschreibt auf Verlangen Umfang und Ursache.

12.4 Gesetzliche Aufbewahrungspflichten gelten nur für die eigenen Geschäftsdaten des Miners und rechtfertigen nie die Speicherung von Inhalten.

## 13. Verzeichnisse und Kontakt

Der Miner führt die nach Art. 30 Abs. 2 DSGVO erforderlichen Verzeichnisse und benennt in Anlage 4 einen Datenschutzkontakt (und einen Datenschutzbeauftragten, wenn das Gesetz einen vorschreibt). Der Kontakt des Betreibers ist info@productivity-boost.com.

## 14. Haftung

14.1 Die Haftung gegenüber betroffenen Personen richtet sich nach Art. 82 DSGVO. Zwischen den Parteien gelten Art. 82 Abs. 5 DSGVO und die gesetzlichen Vorschriften über den Rückgriff.

14.2 Der Miner haftet dem Betreiber nach den gesetzlichen Vorschriften für Verstöße gegen diesen Vertrag durch ihn selbst und seine Unterauftragsverarbeiter. Er stellt den Betreiber von Ansprüchen Dritter (insbesondere Kunden, betroffener Personen und Behörden, einschließlich Bußgeldern) und von angemessenen Verteidigungskosten frei, soweit diese durch einen Verstoß des Miners oder seiner Unterauftragsverarbeiter gegen diesen Vertrag oder das Datenschutzrecht verursacht sind. Der Betreiber informiert den Miner unverzüglich über solche Ansprüche und hört ihn vor einem Vergleich an.

14.3 Der Betreiber haftet unbeschränkt für Vorsatz und grobe Fahrlässigkeit, für die Verletzung des Lebens, des Körpers oder der Gesundheit, nach dem Produkthaftungsgesetz, für übernommene Garantien und soweit zwingendes Recht dies vorschreibt. Bei leichter Fahrlässigkeit haftet der Betreiber nur für die Verletzung einer wesentlichen Vertragspflicht (einer Pflicht, deren Erfüllung die ordnungsgemäße Durchführung des Vertrags überhaupt erst ermöglicht und auf deren Einhaltung die andere Partei regelmäßig vertrauen darf), und dann begrenzt auf den vorhersehbaren, für diese Art von Vertrag typischen Schaden. Abschnitt 2 bleibt unberührt: Weil der Vertrag keinen Anspruch auf Weiterleitung oder auf Belohnungen gibt, schuldet der Betreiber keinen Ersatz für Belohnungen oder erwartete Vorteile, die nicht entstehen, weil die Weiterleitung eingeschränkt, ausgesetzt oder beendet wird.

## 15. Laufzeit und Kündigung

15.1 Dieser Vertrag wird mit der Annahme wirksam (Datum im Abschlussprotokoll) und läuft auf unbestimmte Zeit.

15.2 Jede Partei kann diesen Vertrag in Textform mit einer Frist von 14 Tagen kündigen.

15.3 Der Betreiber kann die Weiterleitung jederzeit nach Abschnitt 2.1 beenden. Die Beendigung der Weiterleitung beendet diesen Vertrag nicht, es sei denn, der Betreiber erklärt die Kündigung; die Pflichten des Miners bestehen fort, solange sich Inhalte in seinen Systemen befinden.

15.4 Jede Partei kann aus wichtigem Grund fristlos kündigen (§ 314 BGB). Ein wichtiger Grund besteht für den Betreiber insbesondere, wenn der Miner gegen die Abschnitte 3, 4, 6 oder 10 verstößt, unzutreffende Angaben zu seinem Unternehmen oder seinen Standorten gemacht hat, die Kontrolle über den Hotkey oder die Endpunkte verliert, zahlungsunfähig wird, oder wenn der Betreiber aufgrund Gesetzes, behördlicher Anordnung oder eines Kundenwiderspruchs die Nutzung des Miners beenden muss.

15.5 Nach Beendigung dieses Vertrags gilt Abschnitt 12. Die Abschnitte 5, 12, 14 und 17 sowie die Pflichten des Miners aus Abschnitt 4 für noch in seinem Besitz befindliche Inhalte gelten fort.

## 16. Änderungen

16.1 Der Betreiber darf diesen Vertrag aus rechtlichen oder regulatorischen Gründen, wegen Änderungen des Kunden-AVV oder wegen des technischen Fortschritts beim Schutz von Inhalten ändern, indem er die neue Version mindestens 45 Tage im Voraus in Textform ankündigt. Der Miner kann innerhalb von 30 Tagen in Textform widersprechen. Ohne Widerspruch innerhalb dieser Frist gilt die neue Version ab dem genannten Datum; die Ankündigung weist darauf hin.

16.2 Widerspricht der Miner, gilt die bisherige Version weiter, der Betreiber kann aber die Weiterleitung beenden oder diesen Vertrag fristlos kündigen, wenn die Änderung rechtlich erforderlich ist.

16.3 Änderungen von Standorten, Endpunkten, Hotkeys und Unterauftragsverarbeitern richten sich nach den Abschnitten 3.6 und 8; die Zustimmung des Betreibers zu einer aktualisierten Anlage 4 erfolgt in Textform.

## 17. Schlussbestimmungen

17.1 Dieser Vertrag wird in der im Abschlussprotokoll oben beschriebenen elektronischen Form geschlossen. Mitteilungen nach diesem Vertrag erfolgen in Textform an die Kontakte in Anlage 4; an den Betreiber an info@productivity-boost.com.

17.2 Für die Verarbeitung von Inhalten geht dieser Vertrag anderen Bedingungen der Parteien und etwaigen Bedingungen des Miners vor. Die Protokollregeln des Netzwerks regeln nur das Verhältnis des Miners zum Netzwerk und gehen diesem Vertrag nicht vor.

17.3 Der Miner darf Rechte oder Pflichten aus diesem Vertrag nicht ohne vorherige Zustimmung des Betreibers in Textform übertragen.

17.4 Es gilt deutsches Recht unter Ausschluss des UN-Kaufrechts und der Kollisionsnormen. Gerichtsstand für Streitigkeiten aus oder im Zusammenhang mit diesem Vertrag ist Passau, wenn der Miner Kaufmann, juristische Person des öffentlichen Rechts oder öffentlich-rechtliches Sondervermögen ist, und, soweit zulässig, auch für Miner mit Sitz in einem anderen Mitgliedstaat. Der Betreiber kann den Miner auch an dessen Sitz verklagen.

17.5 Dieser Vertrag besteht in englischer und deutscher Sprache. Weichen die Fassungen voneinander ab, geht die deutsche Fassung vor.

17.6 Ist eine Bestimmung dieses Vertrags unwirksam, bleibt der Rest wirksam. An die Stelle der unwirksamen Bestimmung tritt die wirksame Bestimmung, die ihrem Zweck am nächsten kommt.

## Anlage 1 — Einzelheiten der Verarbeitung

1. **Gegenstand und Zweck:** Inferenz für typisierte Entscheidungen. Der Betreiber (für seine Kunden) sendet einen Zustand (Text und, soweit unterstützt, Bilder), eine Frage und Antwortoptionen an den Endpunkt des Miners; das vom Miner betriebene Modell berechnet Wahrscheinlichkeiten für die Antwortoptionen und gibt sie an den Betreiber zurück. Zweck ist ausschließlich, dieses Ergebnis bereitzustellen.

2. **Art der Verarbeitung:** Empfang über eine verschlüsselte Verbindung, vorübergehende Haltung im Arbeitsspeicher der Inferenzserver des Miners (System- und GPU-Speicher), Berechnung durch das Modell, Rückgabe des Ergebnisses, Löschung. Keine Speicherung von Inhalten.

3. **Arten personenbezogener Daten:** werden von den Kunden des Betreibers bestimmt. Typischerweise alle personenbezogenen Daten in den übermittelten Texten oder Bildern, zum Beispiel Namen, Kontaktdaten, Inhalte von Nachrichten, Tickets, Dokumenten oder Transaktionen, Beschreibungen von Verhalten oder Präferenzen und Bilder, die Personen zeigen können. Besondere Kategorien personenbezogener Daten (Art. 9 DSGVO) nur, soweit der Kunde eine Rechtsgrundlage hat und die Maßnahmen als angemessen beurteilt hat.

4. **Kategorien betroffener Personen:** werden von den Kunden des Betreibers bestimmt. Typischerweise deren Kunden, Nutzer, Interessenten, Beschäftigte, Auftragnehmer und Geschäftspartner sowie andere in den übermittelten Inhalten genannte Personen.

5. **Speicherung von Inhalten:** keine (Zero Retention). Inhalte und Ergebnisse werden nicht in Logs, Datenbanken, Datenträger oder sonstigen dauerhaften Speicher geschrieben. Sie werden im flüchtigen Arbeitsspeicher gehalten, solange die Anfrage verarbeitet wird. Zur Leistungssteigerung darf der Inferenzserver Zwischenwerte aktueller Anfragen im GPU-Speicher vorhalten (Prefix-Cache), bis sie von späteren Anfragen überschrieben werden, spätestens bis zum Neustart des Serverprozesses; dieser Cache wird nie persistiert, ist je Modellinstanz isoliert und kann über die API nicht ausgelesen werden. Metadaten ohne Inhalte: Abschnitt 6.6.

6. **Ort der Verarbeitung:** ausschließlich die in Anlage 4 genannten Standorte in der EU/im EWR.

7. **Dauer:** für die Laufzeit dieses Vertrags und bis zur Löschung nach Abschnitt 12.

8. **Datenschutzkontakt beim Betreiber:** info@productivity-boost.com.

## Anlage 2 — Technische und organisatorische Maßnahmen (Art. 32 DSGVO)

### Teil A — Mindestmaßnahmen, zu denen sich der Miner verpflichtet

**A.1 Verschlüsselung (Art. 32 Abs. 1 lit. a)**

- Alle Endpunkte sind nur über TLS 1.2 oder höher erreichbar; unverschlüsseltes HTTP wird abgelehnt.
- Verbindungen zwischen Komponenten, die Inhalte verarbeiten (Proxy, Inferenzserver, Tunnel), sind verschlüsselt und authentifiziert.
- Alle Datenträger und Volumes von Systemen, die Inhalte verarbeiten, verwenden Festplattenvollverschlüsselung; die Schlüssel liegen nicht auf demselben Datenträger.

**A.2 Vertraulichkeit (Art. 32 Abs. 1 lit. b)**

- Zutrittskontrolle: Die Hardware steht in den in Anlage 4 genannten Rechenzentren, in verschlossenen Racks oder Käfigen mit Zutrittskontrolle und Protokollierung durch den Rechenzentrumsbetreiber.
- Zugangskontrolle: administrativer Zugang nur über SSH mit öffentlichen Schlüsseln oder eine Konsole mit Multi-Faktor-Authentifizierung (MFA); keine Passwort-Logins; Firewalls lassen nur die erforderlichen Ports zu.
- Administrativer Zugriff nur aus der EU/dem EWR: Administrativer Zugriff auf Systeme, die Inhalte verarbeiten, erfolgt nur von Geräten und Personen, die sich in der EU/im EWR befinden.
- Zugriffskontrolle: namentlich benannte Administratoren, Need-to-know, rollenbasiert, Zugriffe mindestens einmal jährlich überprüft; keine gemeinsam genutzten Konten.
- Isolation des Inferenzprozesses: Der Inferenzprozess läuft unter einem eigenen unprivilegierten Benutzer oder in einem eigenen Container oder einer eigenen virtuellen Maschine, ohne gemeinsame Dateisysteme mit anderen Workloads, ohne Workloads anderer Mandanten oder Dritter auf derselben GPU oder demselben Host und nur mit den benötigten Netzwerkpfaden.
- Keine Inhalte in Entwicklungs- oder Testsystemen.
- Keine Inhalts-Logs: Logs enthalten nur IDs, Größen, Latenz, Modell und Status, nie Anfrage- oder Antwortinhalte; Debug- und Trace-Modi, die Körper aufzeichnen, sind deaktiviert; keine Inhalte in Monitoring, Tracing oder Absturzberichten.

**A.3 Integrität (Art. 32 Abs. 1 lit. b)**

- Weitergabekontrolle: Verschlüsselung bei der Übertragung (A.1); keine Wechselmedien für Inhalte.
- Eingabekontrolle: Administrative Handlungen und Konfigurationsänderungen werden protokolliert.
- Modellgewichte und Container-Images sind die vom Netzwerkprotokoll geforderten und werden per Prüfsumme verifiziert; der Miner verändert Ergebnisse nicht.

**A.4 Verfügbarkeit und Belastbarkeit (Art. 32 Abs. 1 lit. b und c)**

- Überwachung der Dienste mit automatischem Neustart ausgefallener Prozesse.
- Patching: Sicherheitsupdates für Betriebssystem, GPU-Treiber, Inferenzsoftware und exponierte Dienste werden unverzüglich eingespielt; kritische Updates spätestens 7 Tage nach Veröffentlichung, übrige Sicherheitsupdates innerhalb von 30 Tagen.
- Backups, falls vorhanden, enthalten nur Konfiguration, nie Inhalte.

**A.5 Schutz der Schlüssel**

- Der Hotkey und alle weiteren Signatur- oder Authentifizierungsschlüssel werden verschlüsselt oder in einem geschützten Schlüsselspeicher aufbewahrt, auf den nur namentlich benannte Personen zugreifen können, sie liegen nicht im Quellcode oder in Logs und werden nicht an Dritte weitergegeben.
- Verlust, Verdacht der Kompromittierung oder unbefugte Nutzung eines Schlüssels wird nach Abschnitt 10.2 gemeldet, und der Schlüssel wird unverzüglich ausgetauscht.

**A.6 Regelmäßige Überprüfung und Bewertung (Art. 32 Abs. 1 lit. d)**

- Schwachstellenscans der exponierten Systeme und Überprüfung dieser Maßnahmen mindestens einmal jährlich und nach jedem Sicherheitsvorfall.
- Dokumentierter Vorfallprozess: Erkennung, Eindämmung, Bewertung, Meldung an den Betreiber innerhalb von 24 Stunden (Abschnitt 10.2), Nachbereitung.

**A.7 Organisatorische Maßnahmen**

- Alle Personen mit Zugriff sind zur Vertraulichkeit verpflichtet und im Datenschutz unterwiesen.
- Verträge nach Art. 28 DSGVO mit Unterauftragsverarbeitern werden geschlossen, bevor diese Zugang erhalten (Abschnitt 8.4).
- Administratorgeräte nutzen Festplattenvollverschlüsselung, Bildschirmsperre und aktuelle Sicherheitsupdates.
- Geheimnisse werden in geschützten Speichern gehalten, nie im Quellcode oder in Logs.

### Teil B — Eigene Beschreibung der Maßnahmen durch den Miner

{{tom_statement}}

## Anlage 3 — Unterauftragsverarbeiter des Miners

| Unterauftragsverarbeiter (Name, Anschrift) | Leistung | Ort der Verarbeitung | Garantie |
| --- | --- | --- | --- |
{{own_subprocessors}}

Änderungen nur nach Abschnitt 8.

## Anlage 4 — Kontakte, Standorte und Endpunkte

| Angabe | Wert |
| --- | --- |
| Datenschutzkontakt des Miners | {{privacy_contact}} |
| Vertretungsberechtigter Unterzeichner | {{signatory_name}}, {{signatory_role}}, {{signatory_email}} |
| Standorte (Rechenzentren in der EU/im EWR) | {{dc_locations}} |
| Hotkeys (SS58) | {{hotkeys}} |
| Endpunkte | {{endpoints}} |
| Kontakt des Betreibers | info@productivity-boost.com |
