# Vertrag über die Unterauftragsverarbeitung für EU-Miner (Art. 28 Abs. 2 und 4 DSGVO)

Decision Models — REAX-Netzwerk (Bittensor-Subnet 92)

Version {{version}} · Vertrags-ID {{agreement_id}}

*Weichen die Sprachfassungen voneinander ab, geht die deutsche Fassung vor (Abschnitt 17.5).*

## Parteien

**Betreiber („Betreiber“, „Auftragsverarbeiter“ oder „wir“)**

productivity-boost.com Betriebs UG (haftungsbeschränkt) & Co. KG, Reichenberger Str. 2, 94036 Passau, Deutschland, Amtsgericht Passau HRA 12725, vertreten durch ihre persönlich haftende Gesellschafterin productivity-boost.com UG (haftungsbeschränkt) (Amtsgericht Passau HRB 8453), diese vertreten durch ihren Geschäftsführer Florian Standhartinger. Marke: Decision Models (decisionmodels.io). Kontakt für diesen Vertrag: info@productivity-boost.com.

**Miner („Miner“ oder „Unterauftragsverarbeiter“)**

{{miner_company}} ({{miner_legal_form}}), {{miner_address}}, {{miner_country}}, Registereintrag (falls vorhanden): {{miner_register}}, USt-IdNr.: {{miner_vat_id}}, vertreten durch {{signatory_name}} ({{signatory_role}}), E-Mail {{signatory_email}}.

Datenschutzkontakt des Miners: {{privacy_contact}}.

## Abschlussprotokoll

| Angabe | Wert |
| --- | --- |
| Vertrags-ID | {{agreement_id}} |
| Version des Textes | {{version}} |
| Angenommen am (UTC) | {{accepted_at}} |
| SHA-256 des vom Miner angenommenen, ausgefüllten Textes (einschließlich seiner Angaben und der Anlagen; für die Hashbildung zeigen die Felder Vertrags-ID, Angenommen am und SHA-256 die Markierung „wird bei Annahme vergeben“ in eckigen Klammern) | {{text_sha256}} |

Der auf mine.decisionmodels.io veröffentlichte Text dieses Vertrags ist ein dauerhaftes Angebot des Betreibers an Unternehmen, die die Voraussetzungen von Abschnitt 3.1 erfüllen. Der Betreiber ist damit einverstanden, dass der Miner im Formular Angaben macht (Parteiangaben, Anlage 2 Teil B, Anlage 3 und Anlage 4); diese Angaben ändern die Abschnitte 1 bis 17 und Anlage 2 Teil A nicht, die im Konfliktfall vorgehen, und die Nutzung der angegebenen Standorte, Endpunkte, Hotkeys und Unterauftragsverarbeiter setzt die Bestätigung des Betreibers nach den Abschnitten 3.6 und 8.1 voraus. Der Miner nimmt das Angebot durch elektronische Erklärung eines vertretungsberechtigten Unterzeichners an (Name, Funktion, Unternehmen, E-Mail-Adresse und Bestätigung „Ich bin berechtigt, das oben genannte Unternehmen zu vertreten“). Der Vertrag kommt mit Zugang der Annahme im System des Betreibers zustande. Die Verifizierung des Miners (Abschnitt 3.5) ist keine Voraussetzung für den Vertragsschluss; sie ist Voraussetzung für die Weiterleitung (Präambel (D), Abschnitt 2.1) und für die Bestätigung von Standorten, Endpunkten, Hotkeys und Unterauftragsverarbeitern durch den Betreiber (Abschnitte 3.6 und 8.1). Die Annahme wird mit Zeitstempel (UTC), IP-Adresse, Version und dem SHA-256-Hash des dem Unterzeichner angezeigten, ausgefüllten Textes protokolliert. Der Miner erhält den vollständigen Vertrag unmittelbar nach der Annahme als PDF zum Herunterladen; auf Anforderung sendet der Betreiber eine weitere Kopie per E-Mail. Der Vertrag ist damit im Sinne von Art. 28 Abs. 9 DSGVO schriftlich in einem elektronischen Format abgeschlossen.

## Präambel

(A) Der Betreiber erbringt den Inferenzdienst Decision Models (Inferenz für typisierte Entscheidungen: ein Zustand, eine Frage und Antwortoptionen gehen hinein, Wahrscheinlichkeiten kommen heraus). Für seine API-Kunden handelt der Betreiber als Auftragsverarbeiter auf Grundlage seines Auftragsverarbeitungsvertrags (Version 1.2 oder neuer, „Kunden-AVV“).

(B) Der Betreiber kann künftig Anfragen seines EU-Tarifs an unabhängige Unternehmen weiterleiten, die GPU-Hardware in Rechenzentren in der EU betreiben und als Miner am REAX-Netzwerk (Bittensor-Subnet 92) teilnehmen. Ein Miner, der solche Anfragen erhält, verarbeitet personenbezogene Daten im Auftrag des Betreibers und ist dessen Unterauftragsverarbeiter nach Art. 28 Abs. 2 und 4 DSGVO.

(C) Nach Abschnitt 6.3 des Kunden-AVV muss der Betreiber jedem Unterauftragsverarbeiter vertraglich dieselben Datenschutzpflichten auferlegen, die der Kunden-AVV dem Betreiber auferlegt. Dieser Vertrag tut das.

(D) Eine Weiterleitung an einen Miner erfolgt erst, nachdem dieser Vertrag geschlossen wurde, der Miner verifiziert wurde (Unternehmen und Standorte in der EU), der Betreiber die Standorte, Endpunkte, Hotkeys und Unterauftragsverarbeiter nach den Abschnitten 3.6 und 8.1 bestätigt hat, die Frist nach Abschnitt 6.2 des Kunden-AVV (mindestens 30 Tage) abgelaufen ist und eingegangene Widersprüche behandelt wurden und der Betreiber sich für die Weiterleitung entschieden hat.

## 1. Gegenstand, Begriffe, Geltungsbereich

1.1 Dieser Vertrag regelt die Verarbeitung personenbezogener Daten durch den Miner im Auftrag des Betreibers, wenn der Miner Anfragen beantwortet, die der Betreiber (oder ein vom Betreiber betriebenes System) an die in Anlage 4 genannten Endpunkte sendet.

1.2 „Inhalte“ sind alle Daten, die der Miner in einer Anfrage erhält oder für sie erzeugt: Zustände, Fragen, Optionen, Bilder und sonstige Eingaben, die Ergebnisse (Antworten) und alle daraus abgeleiteten Daten, einschließlich Token, Embeddings, Attention- oder Prefix-Cache-Werte, Zwischenwerte und Teilergebnisse.

1.3 „EU“ sind die Mitgliedstaaten der Europäischen Union. „EU/EWR“ sind die Mitgliedstaaten der Europäischen Union und die übrigen Vertragsstaaten des Abkommens über den Europäischen Wirtschaftsraum.

1.4 Gegenstand, Art und Zweck der Verarbeitung, die Arten personenbezogener Daten und die Kategorien betroffener Personen ergeben sich aus Anlage 1. Die Inhalte werden von den Kunden des Betreibers bestimmt und können personenbezogene Daten enthalten.

1.5 Dieser Vertrag gilt für jede Anfrage, die vom Betreiber an einem in Anlage 4 genannten Endpunkt eingeht, gleich welchem Tarif die Anfrage zugeordnet ist, damit der Miner Tarife nicht unterscheiden muss und für alle Inhalte derselbe Schutz gilt.

1.6 Dieser Vertrag regelt nicht die eigenen Geschäftsdaten des Miners (zum Beispiel Kunden-, Buchhaltungs- und Personaldaten) und nicht die öffentlichen Daten des Netzwerkprotokolls (zum Beispiel den öffentlichen Hotkey und Einträge auf der Blockchain). Dafür ist der Miner selbst verantwortlich.

1.7 Der Miner entscheidet nicht über die Zwecke und Mittel der Verarbeitung von Inhalten. Tut er es dennoch, gilt er für diese Verarbeitung als Verantwortlicher (Art. 28 Abs. 10 DSGVO) und verstößt gegen diesen Vertrag.

## 2. Keine Zusage zur Weiterleitung, keine Zahlung, Protokollbelohnungen

2.1 Dieser Vertrag verpflichtet den Betreiber nicht, Anfragen oder ein bestimmtes Volumen an Anfragen an den Miner weiterzuleiten. Die Weiterleitung ist allein Entscheidung des Betreibers. Sie erfolgt erst nach den in Präambel (D) genannten Schritten. Der Betreiber kann die Weiterleitung jederzeit ohne Vorankündigung und ohne Angabe von Gründen einschränken, aussetzen oder beenden, ohne dem Miner gegenüber zu haften.

2.2 Abgesehen von Kostenerstattung nach Abschnitt 11.3 und Haftung nach Abschnitt 14 schuldet der Betreiber dem Miner aus diesem Vertrag keine Zahlung, Gebühr, Vergütung oder Entschädigung. Ob und wie die Protokollregeln des Netzwerks Antworten des Miners berücksichtigen und ob Protokollbelohnungen entstehen, richtet sich ausschließlich nach diesen Regeln und nicht nach diesem Vertrag. Protokollbelohnungen sind keine Gegenleistung aus diesem Vertrag; der Betreiber macht keine Aussage, Zusage oder Garantie zu ihrem Bestehen, ihrer Höhe oder ihrem Wert.

2.3 Der Miner trägt alle eigenen Kosten, einschließlich Hardware, Hosting, Energie, Anbindung, Personal und der Kosten der Vertragserfüllung.

2.4 Dieser Vertrag begründet kein Gesellschafts-, Vertretungs- oder Arbeitsverhältnis, kein Joint Venture und keine Exklusivität für eine der Parteien.

## 3. Anforderungen an den Miner, Standort, keine Übermittlung

3.1 Der Miner bestätigt, dass er eine rechtsfähige juristische Person oder Personengesellschaft mit Sitz in der EU/im EWR ist, die im Rahmen ihrer gewerblichen oder beruflichen Tätigkeit handelt, und dass die Person, die diesen Vertrag annimmt, zu seiner Vertretung berechtigt ist.

3.2 Der Miner betreibt sämtliche Hardware, auf der Inhalte verarbeitet werden (GPUs, CPUs, Arbeitsspeicher, Speicher, Netzwerktechnik), ausschließlich in den in Anlage 4 genannten Rechenzentren, die in Mitgliedstaaten der Europäischen Union liegen (die „Standorte“).

3.3 Inhalte dürfen die Europäische Union nicht verlassen und dürfen nicht von außerhalb der Europäischen Union eingesehen oder abgerufen werden. Das gilt ausnahmslos für Fernadministration, Support- und Wartungszugriffe, Monitoring, Telemetrie und Absturzberichte, Backups, Managed Services, Hersteller- oder Lieferantensupport sowie für Zugriffe verbundener Unternehmen oder von Personal, das sich physisch außerhalb der Europäischen Union befindet, auch auf Reisen. Administrativer Zugriff auf Systeme, die Inhalte verarbeiten, ist nur von Geräten und Personen zulässig, die sich in der Europäischen Union befinden.

3.4 Der Miner leitet Inhalte nicht an Dritte oder an andere Orte weiter, spiegelt oder überträgt sie nicht über Proxys oder Relays und legt sie nicht anderweitig offen, außer gegenüber seinen Unterauftragsverarbeitern nach Anlage 3. Insbesondere nutzt der Miner zur Beantwortung von Anfragen keine Modell-APIs Dritter, keine gemietete oder über Marktplätze vermittelte GPU-Kapazität und keine sonstige Rechenleistung, die nicht in Anlage 3 und Anlage 4 aufgeführt ist.

3.5 Der Miner gibt dem Betreiber zutreffende Auskunft über sein Unternehmen, seine Standorte und seine Systeme und legt auf Verlangen Nachweise vor (zum Beispiel Handelsregisterauszug, USt-IdNr., Rechenzentrumsvertrag oder -rechnung, Netzwerk- oder Hardwareangaben). Der Betreiber darf die Angaben prüfen, auch durch nicht eingreifende technische Prüfungen der Endpunkte (zum Beispiel Netzwerk-Routing, Latenz, TLS-Konfiguration und Antworten auf Protokollanfragen); Penetrations- oder Lasttests bedürfen der vorherigen Zustimmung des Miners in Textform. Der Miner setzt keine VPNs, Tunnel, Proxys oder andere Techniken ein, die den tatsächlichen Standort der Endpunkte oder der Hardware verschleiern.

3.6 Der Miner teilt dem Betreiber jede Änderung seiner Unternehmensangaben, Standorte, Endpunkte oder Hotkeys in Textform mit. Ein neuer oder geänderter Standort, Endpunkt oder Hotkey wird für Inhalte erst verwendet, nachdem der Betreiber ihn in Textform bestätigt hat, und bei neuen Standorten und Unterauftragsverarbeitern erst nach Ablauf der Frist nach Abschnitt 8.2.

## 4. Weisungen

4.1 Der Miner verarbeitet Inhalte nur auf dokumentierte Weisung des Betreibers, auch in Bezug auf Übermittlungen in Drittländer, außer er ist nach Unionsrecht oder dem Recht eines Mitgliedstaats zu anderer Verarbeitung verpflichtet; in diesem Fall teilt der Miner dem Betreiber diese rechtlichen Anforderungen vor der Verarbeitung mit, sofern das betreffende Recht dies nicht wegen eines wichtigen öffentlichen Interesses verbietet (Art. 28 Abs. 3 lit. a DSGVO).

4.2 Die dokumentierten Weisungen des Betreibers sind dieser Vertrag einschließlich seiner Anlagen, die an den Endpunkten im Rahmen der technischen Schnittstelle und des Protokolls des Netzwerks eingehenden Anfragen sowie weitere Weisungen in Textform an den Kontakt des Miners nach Anlage 4.

4.3 Einziger zulässiger Zweck ist, das Ergebnis der Anfrage zu berechnen und an den Absender zurückzugeben. Der Miner nutzt Inhalte nicht zu anderen Zwecken, insbesondere nicht für Training, Fine-Tuning, Distillation, Evaluierung, Benchmarking, Profilbildung, Analyse, Produktverbesserung, Werbung, Weiterverkauf, Veröffentlichung oder die Erstellung von Datensätzen, und wertet Inhalte nicht aus und sieht sie nicht ein.

4.4 Der Miner informiert den Betreiber unverzüglich, wenn er der Auffassung ist, dass eine Weisung gegen die DSGVO oder andere Datenschutzvorschriften verstößt. Er darf die Ausführung der Weisung aussetzen, bis der Betreiber sie bestätigt oder ändert.

4.5 Verlangt eine Behörde oder ein Gericht Zugang zu Inhalten oder zu Systemen, die Inhalte enthalten, informiert der Miner den Betreiber vor jeder Offenlegung unverzüglich, sofern das Gesetz dies nicht verbietet, legt nicht mehr offen, als rechtlich zwingend ist, und verweist die Behörde nach Möglichkeit an den Betreiber.

4.6 Der Betreiber stellt sicher, dass er Inhalte erst nach Abschluss des Verfahrens nach Abschnitt 6.2 des Kunden-AVV an den Miner weiterleitet, informiert den Miner unverzüglich, wenn ein Widerspruch oder eine Weisung eines Kunden erfordert, dass der Miner die Verarbeitung von Anfragen dieses Kunden einstellt, und erteilt keine Weisungen, von denen er weiß, dass sie gegen Datenschutzrecht verstoßen. Für die Rechtmäßigkeit der gesendeten Inhalte sind die Kunden des Betreibers als Verantwortliche und im Verhältnis zum Miner der Betreiber verantwortlich; der Miner ist nicht verpflichtet, sie zu prüfen.

## 5. Vertraulichkeit

Der Miner stellt sicher, dass alle Personen, die zur Verarbeitung von Inhalten befugt sind, auch die seiner Unterauftragsverarbeiter, sich zur Vertraulichkeit verpflichtet haben oder einer angemessenen gesetzlichen Verschwiegenheitspflicht unterliegen (Art. 28 Abs. 3 lit. b DSGVO), dass sie Inhalte nur auf Weisung des Betreibers verarbeiten (Art. 29, Art. 32 Abs. 4 DSGVO) und dass der Zugriff auf das für den Betrieb der Systeme unbedingt Erforderliche beschränkt ist. Im Normalbetrieb sieht niemand Inhalte ein. Die Vertraulichkeitspflicht besteht nach Beendigung dieses Vertrags fort.

## 6. Keine Speicherung von Inhalten

6.1 Inhalte werden nur im flüchtigen Arbeitsspeicher (System- und GPU-Speicher) gehalten, solange die Anfrage verarbeitet wird. Sie werden nicht in Logs, Datenbanken, Dateien, Datenträger, Swap-Speicher, Core- oder Absturz-Dumps, Warteschlangen, Message-Broker, Caches, Monitoring-, Tracing- oder Fehlerberichtssysteme, Backups, Snapshots oder sonstigen dauerhaften Speicher geschrieben.

6.2 Der Miner konfiguriert alle Komponenten (Inferenzserver, Laufzeitumgebung, Reverse-Proxys, Load Balancer, Firewalls, Monitoring) so, dass keine Inhalte protokolliert werden. Debug-, Verbose- und Trace-Modi, die Anfrage- oder Antwortkörper aufzeichnen, sind deaktiviert. Fehlermeldungen und Metriken enthalten keine Inhalte.

6.3 Zur Leistungssteigerung darf der Inferenzserver Zwischenwerte aktueller Anfragen im GPU-Speicher vorhalten (Prefix-Cache), bis sie von späteren Anfragen überschrieben werden, spätestens bis zum Neustart des Serverprozesses. Dieser Cache wird nie persistiert, ist je Modellinstanz isoliert und kann über die API nicht ausgelesen werden. Beantwortet derselbe Inferenzprozess auch Anfragen anderer Netzwerkteilnehmer, stellt der Miner sicher, dass Cache-Werte aus Anfragen des Betreibers für Anfragen anderer nicht wiederverwendet und über diese nicht erkennbar werden — durch eine eigene Inferenzinstanz für Anfragen des Betreibers oder durch eine Trennung des Caches je Absender (zum Beispiel einen Cache-Salt je Absender) — oder deaktiviert das Prefix-Caching.

6.4 Swap-Speicher ist deaktiviert oder mit einem Schlüssel verschlüsselt, der beim Neustart verworfen wird; Core- und Absturz-Dumps, die Speicherinhalte enthalten könnten, sind deaktiviert.

6.5 Der Miner kopiert, erfasst, spiegelt, greift ab oder zeichnet Inhalte nicht auf, auch nicht durch Paketmitschnitte, TLS-Interception mit Speicherung der Nutzdaten oder Screenshots.

6.6 Der Miner darf technische Metadaten ohne Inhalte (zum Beispiel Zeitpunkt, Größe, Latenz, Status, Fehlercodes) für Betrieb, Sicherheit und das Protokoll verarbeiten. Metadaten dürfen keine Inhalte enthalten und werden spätestens nach 14 Tagen gelöscht, außer ein konkreter Sicherheitsvorfall erfordert, einzelne Einträge zur Aufklärung länger aufzubewahren.

## 7. Technische und organisatorische Maßnahmen

7.1 Der Miner trifft alle nach Art. 32 DSGVO erforderlichen Maßnahmen. Die mindestens geltenden Maßnahmen ergeben sich aus Anlage 2 Teil A. Teil B enthält die eigene Beschreibung der Maßnahmen durch den Miner; sie ergänzt Teil A und mindert ihn nicht. Widerspricht Teil B oder eine sonstige Angabe des Miners diesem Vertrag oder Teil A, gehen dieser Vertrag und Teil A vor.

7.2 Die Maßnahmen unterliegen dem technischen Fortschritt. Der Miner darf alternative angemessene Maßnahmen umsetzen, wenn das Sicherheitsniveau nicht sinkt. Wesentliche Änderungen teilt er dem Betreiber in Textform mit.

7.3 Der Miner überprüft die Maßnahmen mindestens einmal jährlich und nach jedem Sicherheitsvorfall und dokumentiert die Überprüfung.

## 8. Unterauftragsverarbeiter des Miners

8.1 Der Betreiber erteilt dem Miner die allgemeine schriftliche Genehmigung, die in Anlage 3 aufgeführten Unterauftragsverarbeiter einzusetzen (Art. 28 Abs. 2 DSGVO). Anlage 3 enthält insbesondere den Betreiber jedes Rechenzentrums oder jeder Colocation-Einrichtung, in der die Hardware des Miners steht, und jeden Cloud- oder Hosting-Anbieter, auch wenn dieser nur physischen Zugang zur Hardware hat. Nebenleistungen ohne jeden Zugang zu Inhalten oder zu den Systemen, die sie verarbeiten (zum Beispiel Strom oder Netzwerk-Transit), sind keine Unterauftragsverarbeitung. Die Genehmigung der vom Miner bei der Annahme eingetragenen Unterauftragsverarbeiter sowie die Nutzung der in Anlage 4 eingetragenen Standorte, Endpunkte und Hotkeys werden wirksam, wenn der Betreiber sie nach der Verifizierung in Textform bestätigt. Bis dahin werden keine Inhalte an den Miner weitergeleitet.

8.2 Der Miner informiert den Betreiber in Textform über jede beabsichtigte Hinzuziehung oder Ersetzung eines Unterauftragsverarbeiters mindestens 45 Tage, bevor die Änderung wirksam wird, unter Angabe von Name, Anschrift, Leistung, Standort und Garantien. Der Betreiber benötigt diese Frist, um seine Kunden 30 Tage im Voraus zu informieren. Der Betreiber kann jederzeit, bevor die Änderung wirksam wird, aus Datenschutzgründen widersprechen. Widerspricht der Betreiber, setzt der Miner den neuen Unterauftragsverarbeiter nicht für Inhalte des Betreibers ein; der Betreiber kann zusätzlich die Weiterleitung beenden oder nach Abschnitt 15 kündigen.

8.3 Unterauftragsverarbeiter müssen ihren Sitz in der EU/im EWR haben, Inhalte nur in der EU verarbeiten und dürfen nicht von außerhalb der EU zugänglich sein. In dringenden Fällen, etwa beim plötzlichen Ausfall eines Unterauftragsverarbeiters, darf der Miner ihn durch einen Anbieter ersetzen, der die Anforderungen dieses Abschnitts erfüllt, sofern er den Betreiber vor dem Einsatz informiert; das Widerspruchsrecht des Betreibers und sein Recht, die Weiterleitung zu beenden, bleiben unberührt.

8.4 Der Miner erlegt jedem Unterauftragsverarbeiter vertraglich dieselben Datenschutzpflichten auf, die in diesem Vertrag festgelegt sind, insbesondere hinreichende Garantien für geeignete technische und organisatorische Maßnahmen, die Standortanforderung nach Abschnitt 8.3, das Speicherverbot sowie die Prüf- und Auskunftsrechte (Art. 28 Abs. 4 DSGVO). Er legt dem Betreiber auf Verlangen die maßgeblichen Teile dieses Vertrags vor.

8.5 Der Miner haftet gegenüber dem Betreiber in vollem Umfang dafür, dass seine Unterauftragsverarbeiter ihre Pflichten erfüllen.

## 9. Unterstützung bei Betroffenenrechten

9.1 Unter Berücksichtigung der Art der Verarbeitung unterstützt der Miner den Betreiber mit geeigneten technischen und organisatorischen Maßnahmen, soweit möglich, bei der Beantwortung von Anträgen betroffener Personen nach Kapitel III DSGVO (Art. 28 Abs. 3 lit. e DSGVO). Weil Inhalte nicht gespeichert werden (Abschnitt 6), gibt es normalerweise keine gespeicherten Inhalte, die auszukunften, zu berichtigen oder zu löschen wären. Der Miner bestätigt dies auf Verlangen in Textform.

9.2 Wendet sich eine betroffene Person oder ein Dritter wegen Inhalten unmittelbar an den Miner, leitet er die Anfrage unverzüglich, spätestens innerhalb von zwei Arbeitstagen (Montag bis Freitag, ausgenommen gesetzliche Feiertage am Sitz des Miners), an den Betreiber weiter und beantwortet sie nicht selbst, außer er ist dazu angewiesen.

## 10. Unterstützung nach Art. 32 bis 36 DSGVO; Verletzungen des Schutzes personenbezogener Daten

10.1 Der Miner unterstützt den Betreiber bei der Einhaltung der Art. 32 bis 36 DSGVO unter Berücksichtigung der Art der Verarbeitung und der ihm zur Verfügung stehenden Informationen (Art. 28 Abs. 3 lit. f DSGVO). Dazu gehört, die für eine Datenschutz-Folgenabschätzung und eine vorherige Konsultation erforderlichen Informationen bereitzustellen.

10.2 Der Miner meldet dem Betreiber an info@productivity-boost.com unverzüglich, spätestens innerhalb von 24 Stunden, nachdem ihm eine Verletzung des Schutzes personenbezogener Daten bekannt wurde, die Inhalte betrifft, oder ein Vorfall, der den begründeten Verdacht einer solchen Verletzung ergibt. Dazu zählen unbefugter Zugriff auf Systeme, die Inhalte verarbeiten, Kompromittierung oder Kontrollverlust über den Hotkey oder einen Endpunkt, das Auffinden von Inhalten in Logs oder Speichern, Verarbeitung oder Zugriff außerhalb der EU, Verlust, Diebstahl oder Beschlagnahme von Hardware sowie Verletzungen bei einem Unterauftragsverarbeiter.

10.3 Die Meldung enthält, soweit verfügbar: eine Beschreibung der Art der Verletzung einschließlich der Kategorien und der ungefähren Zahl der betroffenen Personen und Datensätze; Name und Kontaktdaten einer Anlaufstelle; die wahrscheinlichen Folgen; und die ergriffenen oder vorgeschlagenen Maßnahmen zur Behebung und zur Abmilderung der Folgen. Noch nicht verfügbare Informationen werden schrittweise ohne unangemessene weitere Verzögerung nachgereicht.

10.4 Der Miner trifft die erforderlichen Maßnahmen zur Sicherung der Systeme und zur Minderung möglicher nachteiliger Folgen und dokumentiert die Verletzung. Der Miner meldet nicht im Namen des Betreibers oder seiner Kunden an Aufsichtsbehörden, betroffene Personen oder Dritte, außer der Betreiber weist ihn dazu an oder der Miner ist selbst gesetzlich dazu verpflichtet.

10.5 Der Miner informiert den Betreiber unverzüglich über jeden sonstigen Verstoß gegen diesen Vertrag, zum Beispiel unbeabsichtigte Speicherung von Inhalten.

10.6 Jede Partei trägt die eigenen Kosten der Unterstützung nach den Abschnitten 9 und 10.

## 11. Prüfungen und Auskünfte

11.1 Der Miner stellt dem Betreiber alle erforderlichen Informationen zum Nachweis der Einhaltung von Art. 28 DSGVO zur Verfügung und ermöglicht Überprüfungen, einschließlich Inspektionen, die vom Betreiber oder einem vom Betreiber beauftragten Prüfer durchgeführt werden, und trägt dazu bei (Art. 28 Abs. 3 lit. h DSGVO). Das dient auch dem Betreiber dazu, Prüfrechte seiner eigenen Kunden nach Abschnitt 10 des Kunden-AVV zu erfüllen.

11.2 Der Miner darf zunächst aktuelle Unterlagen vorlegen: diesen Vertrag, die technischen und organisatorischen Maßnahmen, die Liste der Unterauftragsverarbeiter, Nachweise über die Standorte und, soweit verfügbar, Zertifikate oder Prüfberichte seiner Unterauftragsverarbeiter (zum Beispiel ISO/IEC-27001-Zertifikate der Rechenzentrumsbetreiber). Reichen diese Unterlagen zum Nachweis der Einhaltung nicht aus, darf der Betreiber Inspektionen durchführen, auch vor Ort sowie als Fernprüfung der Systemkonfiguration. Der Betreiber kündigt Inspektionen mit angemessener Frist an, in der Regel 14 Tage, oder unverzüglich, wenn ein besonderer Anlass vorliegt, etwa eine Verletzung des Schutzes personenbezogener Daten oder eine Anfrage einer Aufsichtsbehörde. Inspektionen finden während der üblichen Geschäftszeiten statt und vermeiden unnötige Störungen des Betriebs. Prüfer müssen zur Vertraulichkeit verpflichtet sein; der Miner darf einem Prüfer widersprechen, der sein direkter Wettbewerber ist, woraufhin der Betreiber einen anderen Prüfer benennt. Fernprüfungen erfolgen, indem Personal des Miners Konfiguration und Logs in einer Bildschirmfreigabe vorführt oder Exporte bereitstellt; der Betreiber erhält keinen eigenständigen Zugang zu Produktivsystemen. Inspektionen vor Ort in Rechenzentren Dritter unterliegen den Zutrittsregeln des Rechenzentrumsbetreibers. Prüfer erhalten keinen Zugriff auf Inhalte oder auf Daten anderer Kunden des Miners.

11.3 Jede Partei trägt die eigenen Kosten von Inspektionen. Der Miner darf angemessene, nachgewiesene Kosten seiner Unterstützung berechnen, wenn der Betreiber ohne besonderen Anlass mehr als eine Inspektion pro Kalenderjahr durchführt, es sei denn, eine Inspektion deckt einen wesentlichen Verstoß des Miners auf.

11.4 Der Miner arbeitet auf Anfrage mit Aufsichtsbehörden zusammen (Art. 31 DSGVO). Rechte der Aufsichtsbehörden bleiben unberührt.

11.5 Der Betreiber behandelt nicht öffentliche Informationen, die er vom Miner nach den Abschnitten 3.5, 8.4 und 11 erhält, vertraulich, nutzt sie nur zur Prüfung und zum Nachweis der Einhaltung dieses Vertrags und des Datenschutzrechts und gibt sie nur an seine Prüfer und Rechtsberater, an Aufsichtsbehörden und — soweit für Abschnitt 10 des Kunden-AVV erforderlich — an zur Vertraulichkeit verpflichtete Kunden weiter. Der Betreiber verarbeitet die personenbezogenen Daten des Unterzeichners und der Kontaktpersonen des Miners wie in seiner auf decisionmodels.io veröffentlichten Datenschutzerklärung beschrieben.

## 12. Löschung und Rückgabe nach Ende der Verarbeitung

12.1 Inhalte werden gelöscht, sobald die Antwort zurückgegeben wurde, vorbehaltlich Abschnitt 6.3. Bei Vertragsende bleiben daher keine Inhalte zurückzugeben oder zu löschen. Der Betreiber wählt hiermit die Löschung; eine Rückgabe scheidet aus, weil keine Inhalte gespeichert werden.

12.2 Bei Beendigung dieses Vertrags oder früher, wenn die Weiterleitung beendet ist und der Betreiber dies verlangt, startet der Miner die Inferenzprozesse neu, leert den Speicher, der Inhalte gehalten hat, und bestätigt innerhalb von 14 Tagen in Textform, dass keine Inhalte verblieben sind.

12.3 Stellt der Miner fest, dass Inhalte entgegen diesem Vertrag gespeichert wurden, löscht er sie unverzüglich, informiert den Betreiber nach Abschnitt 10 und beschreibt auf Verlangen Umfang und Ursache.

12.4 Gesetzliche Aufbewahrungspflichten gelten nur für die eigenen Geschäftsdaten des Miners und rechtfertigen nie die Speicherung von Inhalten.

## 13. Verzeichnisse und Kontakt

Der Miner führt die nach Art. 30 Abs. 2 DSGVO erforderlichen Verzeichnisse und benennt in Anlage 4 einen Datenschutzkontakt (und einen Datenschutzbeauftragten, wenn das Gesetz einen vorschreibt). Der Kontakt des Betreibers ist info@productivity-boost.com.

## 14. Haftung

14.1 Die Haftung gegenüber betroffenen Personen richtet sich nach Art. 82 DSGVO. Zwischen den Parteien gelten Art. 82 Abs. 5 DSGVO und die gesetzlichen Vorschriften über den Rückgriff.

14.2 Der Miner haftet dem Betreiber nach den gesetzlichen Vorschriften für Verstöße gegen diesen Vertrag durch ihn selbst und seine Unterauftragsverarbeiter, vorbehaltlich Abschnitt 14.3. Soweit der Miner einen Verstoß gegen diesen Vertrag oder das Datenschutzrecht (durch ihn selbst oder seine Unterauftragsverarbeiter) zu vertreten hat, stellt er den Betreiber von Ansprüchen Dritter (insbesondere von Kunden und betroffenen Personen) und von angemessenen Kosten der Rechtsverteidigung frei. Gegen den Betreiber verhängte Bußgelder sind nur erfasst, soweit sie auf den Verstoß des Miners zurückgehen und ein Rückgriff rechtlich zulässig ist. Der Betreiber informiert den Miner unverzüglich über solche Ansprüche, ermöglicht ihm die Beteiligung an der Abwehr und erkennt sie ohne Zustimmung des Miners, die nicht unbillig verweigert werden darf, weder an noch vergleicht er sich darüber. § 254 BGB bleibt unberührt.

14.3 Jede Partei haftet unbeschränkt für Vorsatz und grobe Fahrlässigkeit, für die Verletzung des Lebens, des Körpers oder der Gesundheit, nach dem Produkthaftungsgesetz, für übernommene Garantien und soweit zwingendes Recht dies vorschreibt. Im Übrigen haftet eine Partei bei leichter Fahrlässigkeit nur für die Verletzung einer wesentlichen Vertragspflicht (einer Pflicht, deren Erfüllung die ordnungsgemäße Durchführung des Vertrags überhaupt erst ermöglicht und auf deren Einhaltung die andere Partei regelmäßig vertrauen darf), begrenzt auf den vorhersehbaren, für diese Art von Vertrag typischen Schaden und auf 50.000 EUR je Kalenderjahr. Für den Miner sind die Pflichten aus den Abschnitten 3.3, 3.4, 4.3 und 6 wesentliche Vertragspflichten. Die Haftung gegenüber betroffenen Personen nach Art. 82 DSGVO bleibt unberührt. Abschnitt 2 bleibt unberührt: Weil der Vertrag keinen Anspruch auf Weiterleitung oder auf Belohnungen gibt, schuldet der Betreiber keinen Ersatz für Belohnungen oder erwartete Vorteile, die nicht entstehen, weil die Weiterleitung eingeschränkt, ausgesetzt oder beendet wird.

## 15. Laufzeit und Kündigung

15.1 Dieser Vertrag wird mit der Annahme wirksam (Datum im Abschlussprotokoll) und läuft auf unbestimmte Zeit.

15.2 Jede Partei kann diesen Vertrag in Textform mit einer Frist von 14 Tagen kündigen.

15.3 Der Betreiber kann die Weiterleitung jederzeit nach Abschnitt 2.1 beenden. Die Beendigung der Weiterleitung beendet diesen Vertrag nicht, es sei denn, der Betreiber erklärt die Kündigung; die Pflichten des Miners bestehen fort, solange sich Inhalte in seinen Systemen befinden.

15.4 Jede Partei kann aus wichtigem Grund fristlos kündigen (§ 314 BGB). Ein wichtiger Grund besteht für den Betreiber insbesondere, wenn der Miner gegen die Abschnitte 3, 4, 6 oder 10 verstößt, unzutreffende Angaben zu seinem Unternehmen oder seinen Standorten gemacht hat, die Kontrolle über den Hotkey oder die Endpunkte verliert oder wenn eine weitere Weiterleitung an den Miner gegen eine gesetzliche Pflicht oder eine behördliche Anordnung verstieße.

15.5 Nach Beendigung dieses Vertrags gilt Abschnitt 12. Die Abschnitte 5, 10, 11 (für zwölf Monate nach Beendigung), 12, 14 und 17 sowie die Pflichten des Miners aus Abschnitt 4 für noch in seinem Besitz befindliche Inhalte gelten fort.

## 16. Änderungen

16.1 Der Betreiber darf diesen Vertrag ändern, soweit dies aus rechtlichen oder regulatorischen Gründen, wegen Änderungen des Kunden-AVV oder zur Anpassung der technischen und organisatorischen Maßnahmen an den Stand der Technik erforderlich ist, indem er die neue Version mindestens 45 Tage im Voraus in Textform unter Hervorhebung der Änderungen ankündigt. Änderungen, die die Haftung des Miners erweitern, Zahlungspflichten des Miners begründen oder seine Kündigungsrechte einschränken, bedürfen seiner ausdrücklichen Zustimmung. Anderen Änderungen kann der Miner innerhalb von 30 Tagen nach Zugang in Textform widersprechen; ohne Widerspruch innerhalb dieser Frist gilt die neue Version ab dem genannten Datum; die Ankündigung weist darauf hin.

16.2 Widerspricht der Miner, gilt die bisherige Version weiter. Jede Partei kann dann mit einer Frist von 14 Tagen kündigen; ist die Änderung rechtlich erforderlich, kann der Betreiber stattdessen die Weiterleitung mit sofortiger Wirkung beenden.

16.3 Änderungen von Standorten, Endpunkten, Hotkeys und Unterauftragsverarbeitern richten sich nach den Abschnitten 3.6 und 8; die Zustimmung des Betreibers zu einer aktualisierten Anlage 4 erfolgt in Textform.

## 17. Schlussbestimmungen

17.1 Dieser Vertrag wird in der im Abschlussprotokoll oben beschriebenen elektronischen Form geschlossen. Mitteilungen nach diesem Vertrag erfolgen in Textform an die Kontakte in Anlage 4; an den Betreiber an info@productivity-boost.com.

17.2 Für die Verarbeitung von Inhalten geht dieser Vertrag anderen Bedingungen der Parteien und etwaigen Bedingungen des Miners vor. Die Protokollregeln des Netzwerks regeln nur das Verhältnis des Miners zum Netzwerk und gehen diesem Vertrag nicht vor.

17.3 Keine Partei darf Rechte oder Pflichten aus diesem Vertrag ohne vorherige Zustimmung der anderen Partei in Textform übertragen; die Zustimmung darf nicht unbillig verweigert werden; § 354a HGB bleibt unberührt.

17.4 Es gilt deutsches Recht unter Ausschluss des UN-Kaufrechts und der Kollisionsnormen. Gerichtsstand für Streitigkeiten aus oder im Zusammenhang mit diesem Vertrag ist Passau, wenn der Miner Kaufmann, juristische Person des öffentlichen Rechts oder öffentlich-rechtliches Sondervermögen ist, und, soweit zulässig, auch für Miner mit Sitz in einem anderen Mitgliedstaat. Der Betreiber kann den Miner auch an dessen Sitz verklagen.

17.5 Dieser Vertrag besteht in englischer und deutscher Sprache. Weichen die Fassungen voneinander ab, geht die deutsche Fassung vor.

17.6 Ist eine Bestimmung dieses Vertrags unwirksam, bleibt der Rest wirksam. An die Stelle der unwirksamen Bestimmung tritt die wirksame Bestimmung, die ihrem Zweck am nächsten kommt.

## Anlage 1 — Einzelheiten der Verarbeitung

1. **Gegenstand und Zweck:** Inferenz für typisierte Entscheidungen. Der Betreiber (für seine Kunden) sendet einen Zustand (Text und, soweit unterstützt, Bilder), eine Frage und Antwortoptionen an den Endpunkt des Miners; das vom Miner betriebene Modell berechnet Wahrscheinlichkeiten für die Antwortoptionen und gibt sie an den Betreiber zurück. Zweck ist ausschließlich, dieses Ergebnis bereitzustellen.

2. **Art der Verarbeitung:** Empfang über eine verschlüsselte Verbindung, vorübergehende Haltung im Arbeitsspeicher der Inferenzserver des Miners (System- und GPU-Speicher), Berechnung durch das Modell, Rückgabe des Ergebnisses, Löschung. Keine Speicherung von Inhalten.

3. **Arten personenbezogener Daten:** werden von den Kunden des Betreibers bestimmt. Typischerweise alle personenbezogenen Daten in den übermittelten Texten oder Bildern, zum Beispiel Namen, Kontaktdaten, Inhalte von Nachrichten, Tickets, Dokumenten oder Transaktionen, Beschreibungen von Verhalten oder Präferenzen und Bilder, die Personen zeigen können. Besondere Kategorien personenbezogener Daten (Art. 9 DSGVO) nur, soweit der Kunde eine Rechtsgrundlage hat und die Maßnahmen als angemessen beurteilt hat.

4. **Kategorien betroffener Personen:** werden von den Kunden des Betreibers bestimmt. Typischerweise deren Kunden, Nutzer, Interessenten, Beschäftigte, Auftragnehmer und Geschäftspartner sowie andere in den übermittelten Inhalten genannte Personen.

5. **Speicherung von Inhalten:** keine (Zero Retention). Inhalte und Ergebnisse werden nicht in Logs, Datenbanken, Datenträger oder sonstigen dauerhaften Speicher geschrieben. Sie werden im flüchtigen Arbeitsspeicher gehalten, solange die Anfrage verarbeitet wird. Zur Leistungssteigerung darf der Inferenzserver Zwischenwerte aktueller Anfragen im GPU-Speicher vorhalten (Prefix-Cache), bis sie von späteren Anfragen überschrieben werden, spätestens bis zum Neustart des Serverprozesses; dieser Cache wird nie persistiert, ist wie in Abschnitt 6.3 beschrieben isoliert und kann über die API nicht ausgelesen werden. Metadaten ohne Inhalte: Abschnitt 6.6.

6. **Ort der Verarbeitung:** ausschließlich die in Anlage 4 genannten Standorte in Mitgliedstaaten der Europäischen Union; kein Zugriff von außerhalb der EU.

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
- Administrativer Zugriff nur aus der EU: Administrativer Zugriff auf Systeme, die Inhalte verarbeiten, erfolgt nur von Geräten und Personen, die sich in der EU befinden.
- Zugriffskontrolle: namentlich benannte Administratoren, Need-to-know, rollenbasiert, Zugriffe mindestens einmal jährlich überprüft; keine gemeinsam genutzten Konten.
- Isolation des Inferenzprozesses: Der Inferenzprozess läuft unter einem eigenen unprivilegierten Benutzer oder in einem eigenen Container oder einer eigenen virtuellen Maschine, ohne gemeinsame Dateisysteme mit anderen Workloads; keine Workloads Dritter (auch nicht anderer Kunden des Miners) auf derselben GPU; andere Workloads auf demselben Host nur in getrennten virtuellen Maschinen oder Containern ohne Zugriff auf Arbeitsspeicher, GPU oder Netzwerkpfade des Inferenzprozesses; der Inferenzprozess hat nur die benötigten Netzwerkpfade. Die Beantwortung von Anfragen anderer Netzwerkteilnehmer nach dem Protokoll durch denselben Inferenzprozess ist nach Maßgabe von Abschnitt 6.3 zulässig.
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
| Standorte (Rechenzentren in der EU) | {{dc_locations}} |
| Hotkeys (SS58) | {{hotkeys}} |
| Endpunkte | {{endpoints}} |
| Kontakt des Betreibers | info@productivity-boost.com |
