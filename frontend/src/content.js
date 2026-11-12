// All site text. Section entries mirror the CV (Lebenslauf.pdf / CV.pdf).
export const name = "Elias Andrei";
export const email = "aandreielias@gmail.com";
export const github = "https://github.com/aandreielias";

export const projects = [
  {
    id: "verein",
    year: "2026",
    tech: "Java, Spring Boot, TypeScript, Svelte, PostgreSQL, Supabase, Docker, Git",
    images: [
      { src: "uploads/projects/Vereinsmanagement/turniere.png", de: "Turnier mit Gruppentabellen, Ergebnissen und Satzständen", en: "Tournament with group tables, results and set scores" },
      { src: "uploads/projects/Vereinsmanagement/termin.png", de: "Geöffneter Termin mit Ort, Kabine und Karte", en: "Opened appointment with venue, changing room and map" },
      { src: "uploads/projects/Vereinsmanagement/kalender.png", de: "Kalender mit Trainings, Sitzungen, Turnieren und Fristen", en: "Calendar with training sessions, meetings, tournaments and deadlines" },
      { src: "uploads/projects/Vereinsmanagement/aufgaben.png", de: "Aufgaben mit Fälligkeit, Zuständigen und Checklisten", en: "Tasks with due dates, assignees and checklists" },
      { src: "uploads/projects/Vereinsmanagement/mitglieder.png", de: "Mitgliederverwaltung mit Rollen", en: "Member management with roles" },
      { src: "uploads/projects/Vereinsmanagement/sitzungen.png", de: "Laufende Sitzung mit Tagesordnung und geheimer Abstimmung", en: "Running meeting with agenda and secret ballot" },
      { src: "uploads/projects/Vereinsmanagement/inventar.png", de: "Inventar mit Bestand und Lagerort", en: "Inventory with stock and location" },
      { src: "uploads/projects/Vereinsmanagement/start.png", de: "Startseite mit Einrichtung und den nächsten Terminen", en: "Start page with setup steps and the coming week" },
    ],
    de: {
      title: "Vereinsmanagement-Software",
      summary: "Webanwendung (Front- & Backend) zur Verwaltung von Mitgliedern, Terminen, Aufgaben, Aktivitäten, Sitzungen, Dateien und integrierten E-Mails",
      body: [
        "Entwicklung für Soli Deo Gloria Volleyball Vienna, einen Verein in Gründung, den ich mitgegründet habe. Vereinsspezifische Angaben wie Name, Rollen, Ämter und Mitgliedsarten sind Einstellungen, damit die Software auch für andere Vereine nutzbar ist.",
        "Funktionen: Mitglieder mit Rollen und Erziehungsberechtigten für Minderjährige, Vorstand und Ämter, Sitzungen mit Tagesordnung, Protokoll und Beschlüssen, Kalender mit Trainings und Abwesenheiten, Aufgaben, Dateiablage, Inventar, Turniere, Vereins-E-Mail sowie Benachrichtigungen per E-Mail und Push.",
        "Das Backend ist ein modularer Monolith in Spring Boot: eine Anwendung, aufgeteilt in 13 Fachmodule. Jedes Modul ist ein eigenes Paket mit vier Schichten: api (Befehle, Events und DTOs als Records), application (Handler am Bus), domain (Fachlogik in reinem Java) und infrastructure (Datenbankzugriff). Module importieren einander nicht, sie kommunizieren nur über meine Event-Bus-Bibliothek. ArchUnit-Tests prüfen diese Grenzen bei jedem Build.",
        "Über den Bus laufen zwei Arten von Nachrichten. Befehle (club/<modul>/cmd/<name>) haben genau einen Handler, das wird beim Start geprüft; braucht ein Modul Daten eines anderen, fragt es per Request an, etwa Aufgaben bei Mitglieder nach Namen. Events (club/<modul>/evt/<name>) werden erst nach dem Commit der Transaktion veröffentlicht und können beliebig viele Empfänger haben.",
        "Datenhaltung in PostgreSQL (Supabase) mit 145 Flyway-Migrationen, ohne ORM über SQL mit Parametern. Jede Tabelle hat Row-Level-Security, zusätzlich prüft jeder Handler die Berechtigung selbst; Datensätze ohne Zugriff antworten wie nicht vorhanden. Ein Audit-Log hält Änderungen fest, ein Datenbank-Trigger verhindert das Ändern von Einträgen jünger als zwei Jahre. Datenexport und Löschung nach DSGVO laufen über alle Module.",
        "Website und App nutzen dieselbe REST-API. Aus ihrer OpenAPI-Spezifikation werden die TypeScript-Typen des Frontends generiert, ein Integrationstest erkennt ungewollte Änderungen am Vertrag. Fehler kommen einheitlich nach RFC 9457 mit Code und Korrelations-ID.",
        "Frontend in Svelte 5 und TypeScript ohne UI-Framework, ebenfalls mit einem kleinen Event-Bus für Server-Events und UI-Befehle. Ein Demo-Modus bildet die gesamte API im Browser nach, mit denselben Regeln wie der Server; die Abbildungen zeigen diesen Modus mit Testdaten.",
      ],
      diagrams: [
        { src: "uploads/projects/Vereinsmanagement/architektur-de.png", caption: "Systemaufbau: Gateway, Event-Bus, Module, Datenbank und externe Dienste" },
        { src: "uploads/projects/Vereinsmanagement/ablauf-de.png", caption: "Ablauf: Eine Aufgabe wird angelegt" },
      ],
    },
    en: {
      title: "Club management software",
      summary: "Web application (frontend & backend) for managing members, appointments, tasks, activities, meetings, files and integrated email",
      body: [
        "Built for Soli Deo Gloria Volleyball Vienna, a club in formation that I co-founded. Club-specific details such as name, roles, offices and membership types are settings, so other clubs can use the software as well.",
        "Features: members with roles and guardians for minors, board and offices, meetings with agenda, minutes and resolutions, a calendar with training sessions and absences, tasks, file storage, inventory, tournaments, club email and notifications by email and push.",
        "The backend is a modular monolith in Spring Boot: one application, split into 13 domain modules. Each module is its own package with four layers: api (commands, events and DTOs as records), application (handlers on the bus), domain (business logic in plain Java) and infrastructure (database access). Modules do not import each other; they communicate only through my event bus library. ArchUnit tests check these boundaries on every build.",
        "Two kinds of messages travel over the bus. Commands (club/<module>/cmd/<name>) have exactly one handler, which is checked at startup; when a module needs another module's data it sends a request, for example tasks asking members for names. Events (club/<module>/evt/<name>) are published only after the transaction commits and can have any number of receivers.",
        "Data stored in PostgreSQL (Supabase) with 145 Flyway migrations, accessed without an ORM through parameterised SQL. Every table has row-level security, and every handler also checks permissions itself; records without access answer as if they did not exist. An audit log records changes, and a database trigger prevents changing entries younger than two years. GDPR data export and erasure run across all modules.",
        "Website and app use the same REST API. The frontend's TypeScript types are generated from its OpenAPI specification, and an integration test detects unintended changes to the contract. Errors follow RFC 9457 with a code and a correlation ID.",
        "Frontend in Svelte 5 and TypeScript without a UI framework, also with a small event bus for server events and UI commands. A demo mode runs the whole API in the browser with the same rules as the server; the screenshots show this mode with test data.",
      ],
      diagrams: [
        { src: "uploads/projects/Vereinsmanagement/architektur-en.png", caption: "System architecture: gateway, event bus, modules, database and external services" },
        { src: "uploads/projects/Vereinsmanagement/ablauf-en.png", caption: "Request flow: creating a task" },
      ],
    },
  },
  {
    id: "eventbus",
    year: "2026",
    tech: "Java, Maven, JUnit, Git",
    link: "https://github.com/aandreielias/EventBus",
    console: true,
    code: `try (EventBus bus = EventBusBuilder.create().build()) {

    bus.subscribe("orders/created", String.class, orderId -> {
        System.out.println("New order: " + orderId);
    });

    bus.publish("orders/created", "ORD-1042");
}`,
    de: {
      title: "Event-Bus-Bibliothek",
      summary: "Eigenständige Entwicklung einer leichtgewichtigen Java-Bibliothek für asynchrone Event-Kommunikation und Messaging",
      body: [
        "Publish/Subscribe-Bibliothek für Java 21 ohne Laufzeitabhängigkeiten. Komponenten veröffentlichen Nachrichten auf benannten Kanälen, andere abonnieren diese Kanäle; beide Seiten kennen sich nicht. Bestandteil der Backend-Kernarchitektur der Vereinsmanagement-Software, in der alle Module über den Bus kommunizieren.",
        "Kanäle sind Pfade wie orders/eu/de. Beim hierarchischen Routing erhält ein Abonnent von orders auch alle Nachrichten der Unterkanäle. Abonnenten haben eine Priorität und laufen synchron im Thread des Publishers oder asynchron auf virtuellen Threads. Die asynchrone Arbeit ist begrenzt (standardmäßig 10.000 gleichzeitig), darüber läuft sie im Thread des Publishers und bremst ihn statt Arbeit unbegrenzt anzustauen.",
        "Neben Events gibt es Request/Response: ein Handler beantwortet eine Anfrage, der Aufrufer erhält ein CompletableFuture mit Timeout. Fehler werden klar unterschieden, etwa kein Handler, Timeout oder falscher Antworttyp.",
        "Intern delegiert die Klasse DefaultEventBus an austauschbare Strategien für Validierung, Routing, Zustellung und Fehlerbehandlung, die über einen Builder gewählt werden. Kanalnamen werden geprüft (höchstens 16 Ebenen, erlaubte Zeichen). Fehler eines Abonnenten erreichen nie den Publisher, Nachrichten ohne Abonnent gehen an einen Dead-Letter-Handler, und schwache Referenzen melden Abonnenten automatisch ab, sobald ihr Objekt nicht mehr existiert.",
        "Eine Registry zählt Zustellungen und Fehler je Abonnent und führt eine Historie, die nur Metadaten und keine Nutzdaten speichert. Das Kommandozeilenwerkzeug ebus liest sie über JMX aus einer laufenden Anwendung und zeigt Kanäle, Abonnenten, Statistiken und neue Events live an.",
      ],
      diagrams: [{ src: "uploads/projects/EventBus/architektur-de.png", caption: "Aufbau der Bibliothek und Weg einer Nachricht" }],
    },
    en: {
      title: "Event bus library",
      summary: "Independent development of a lightweight Java library for asynchronous event communication and messaging",
      body: [
        "Publish/subscribe library for Java 21 with no runtime dependencies. Components publish messages on named channels, others subscribe to these channels; neither side knows the other. Part of the core backend architecture of the club management software, where all modules communicate through the bus.",
        "Channels are paths such as orders/eu/de. With hierarchical routing, a subscriber of orders also receives all messages of its subchannels. Subscribers have a priority and run either synchronously on the publisher's thread or asynchronously on virtual threads. Asynchronous work is capped (10,000 at once by default); beyond that it runs on the publisher's thread and slows it down instead of piling up unbounded work.",
        "Besides events there is request/response: a handler answers a request, and the caller gets a CompletableFuture with a timeout. Failures are kept distinct, such as no handler, timeout or wrong response type.",
        "Internally the DefaultEventBus class delegates to exchangeable strategies for validation, routing, delivery and error handling, chosen through a builder. Channel names are checked (at most 16 levels, allowed characters). A subscriber's exception never reaches the publisher, messages without a subscriber go to a dead-letter handler, and weak references unsubscribe a subscriber automatically once its object is gone.",
        "A registry counts deliveries and failures per subscriber and keeps a history that stores metadata only, never payloads. The command-line tool ebus reads it over JMX from a running application and shows channels, subscribers, statistics and new events live.",
      ],
      diagrams: [{ src: "uploads/projects/EventBus/architektur-en.png", caption: "Structure of the library and path of a message" }],
    },
  },
  {
    id: "eroots",
    year: "2024",
    tech: "Next.js, Tailwind CSS, MongoDB, AWS S3, Cypress, GitLab CI/CD",
    pdf: "uploads/projects/ERoots/ERoots-Diplomarbeit.pdf#page=129",
    images: [
      { src: "uploads/projects/ERoots/eroots-client-ui.png", de: "Produktkatalog der Kundenansicht", en: "Product catalogue in the customer view" },
      { src: "uploads/projects/ERoots/eroots_architecture.png", de: "Systemarchitektur mit Next.js, MongoDB und AWS S3", en: "System architecture with Next.js, MongoDB and AWS S3" },
    ],
    de: {
      title: "HTL-Diplomarbeit: ERoots",
      summary: "Webanwendung für eine Frauen-Selbsthilfegruppe in Kenia zum Verkauf lokal erzeugter Produkte",
      body: [
        "Diplomarbeit an der HTBLuVA Spengergasse (in englischer Sprache) für die Mutundu Women Self Help Group in Kiambu, Kenia. Die Gruppe wollte mehr Kundschaft erreichen und weniger unverkaufte Ware verlieren.",
        "Umsetzung als Produktkatalog mit Reservierungssystem: Kundinnen und Kunden stellen einen Warenkorb zusammen, bestellen online und bezahlen bei der Abholung. Über ein Admin-Dashboard verwaltet die Gruppe Produkte, Kategorien und Reservierungen ohne technische Vorkenntnisse.",
        "Anwendung mit Next.js und Tailwind CSS, Datenhaltung in MongoDB (Mongoose), Produktbilder in AWS S3, Anmeldung über Google OAuth.",
        "Persönlicher Aufgabenbereich: Deployment, Tests und Qualitätssicherung, mit End-to-End-Tests in Cypress und einer CI/CD-Pipeline in GitLab.",
      ],
    },
    en: {
      title: "HTL diploma thesis: ERoots",
      summary: "Web application for a Kenyan women's self-help group selling their locally sourced products",
      body: [
        "Diploma thesis at HTBLuVA Spengergasse (written in English) for the Mutundu Women Self Help Group in Kiambu, Kenya. The group wanted to reach more customers and lose less unsold produce.",
        "Built as a product catalogue with a reservation system: customers fill a cart, order online and pay on collection. Through an admin dashboard the group manages products, categories and reservations without technical knowledge.",
        "Application in Next.js and Tailwind CSS, data in MongoDB (Mongoose), product images in AWS S3, sign-in with Google OAuth.",
        "Personal responsibilities: deployment, testing and quality control, with end-to-end tests in Cypress and a CI/CD pipeline in GitLab.",
      ],
    },
  },
  {
    id: "portfolio",
    year: "2026",
    tech: "Svelte, JavaScript, Vite, GitHub Actions, Git",
    link: "https://github.com/aandreielias/Portfolio",
    images: [{ src: "uploads/projects/Portfolio/landing.png", de: "Startseite", en: "Landing page" }],
    de: {
      title: "Portfolio-Website",
      summary: "Persönliche Website mit Lebenslauf und Projekten, im Design der Vereinsmanagement-Software",
      body: [
        "Statische Single-Page-Anwendung mit Svelte 5 und Vite, die über GitHub Actions auf GitHub Pages veröffentlicht wird.",
        "Alle Inhalte liegen auf Deutsch und Englisch in einer Datei. Projekte öffnen sich als verschiebbare, skalierbare Fenster, Abbildungen in einer Zoom-Ansicht.",
        "Version 4 (November 2026): Neugestaltung und Neuaufbau mit weniger Komponenten und ohne ungenutzte Abhängigkeiten.",
      ],
    },
    en: {
      title: "Portfolio website",
      summary: "Personal website with CV and projects, in the design of the club management software",
      body: [
        "Static single-page application with Svelte 5 and Vite, published to GitHub Pages through GitHub Actions.",
        "All content is kept in German and English in one file. Projects open as movable, resizable windows, images in a zoom view.",
        "Version 4 (November 2026): new design and rebuild with fewer components and no unused dependencies.",
      ],
    },
  },
];

export const text = {
  de: {
    lang: "de",
    cv: { label: "Lebenslauf (PDF)", href: "uploads/Lebenslauf.pdf" },
    landing: {
      who: "Studiert Software Engineering an der FH Wiener Neustadt und baut Vereinssoftware auf einem eigenen Event-Bus.",
      intro: "Mein größtes Projekt ist eine Software für Vereine: Mitglieder, Kalender und Aufgaben, aufgebaut auf einer Event-Bus-Bibliothek, die ich selbst geschrieben habe.",
      work: "Projekte",
      cv: "Lebenslauf",
      now: "laufend",
      music: { title: "Musik", piece: "Fantasia", by: "Joe Hisaishi, aus „Nausicaä aus dem Tal der Winde“, gespielt 2023", text: "Neben dem Programmieren spiele ich Harfe, seit 2014 an den Wiener Musikschulen, und seit 2018 auch Fagott." },
    },
    ui: { technologies: "Technologien", prev: "Zurück", next: "Weiter", console: "Konsole zum Ausprobieren", close: "Schließen", maximize: "Maximieren", restore: "Verkleinern", openPdf: "Diplomarbeit (PDF)", source: "Quellcode", details: "Details", index: "Inhalt", back: "Zurück" },
    profile: {
      title: "Profil",
      summary: "Software-Engineering-Student mit HTL-Ausbildung im Bereich Biomedizin und Gesundheitsinformatik. Erfahrung in der Entwicklung von Webanwendungen und Java-basierter Software sowie in den Bereichen Softwarearchitektur, Datenbanken und Projektmanagement.",
      rows: [
        ["Interessen", "Musik (Harfe seit 2014, Fagott seit 2018, an den Wiener Musikschulen), Sport"],
      ],
    },
    sections: [
      { id: "projekte", title: "Projekte", kind: "projects" },
      {
        id: "ausbildung",
        title: "Ausbildung",
        entries: [
          { date: "10/2025 – laufend", place: "FH Wiener Neustadt, Biotech Campus Tulln", title: "BSc Software Engineering und Systembau", tech: "Java, Spring Boot, JavaScript, Git, Linux, Algorithmen und Datenstrukturen, Datenbanken, OOP" },
          { date: "2019 – 06/2024", place: "HTBLuVA Spengergasse, Wien", title: "Ausbildungsschwerpunkt Biomedizin und Gesundheitsinformatik", text: ["Diplomarbeit (in englischer Sprache): Creating a Web Application for a Kenyan Women empowerment group selling their locally sourced products", "Persönlicher Aufgabenbereich: Implementation/Development of the deployment, testing and quality control."], tech: "C#, Java, Python, JavaScript, SQL, Spring Boot, Git, Projektmanagement, Frontend- und Backendentwicklung", project: "eroots" },
        ],
      },
      {
        id: "erfahrung",
        title: "Erfahrung",
        entries: [
          { date: "08/2024 – 02/2025", place: "Österreichisches Bundesheer, Hörsching & Wien", title: "Grundwehrdienst" },
          { date: "08/2023", place: "Rehab Zentrum Stadlau, Wien", title: "Praktikum im Bereich Forschung und Entwicklung", text: ["Entwicklung eines EEG-Apparates, Sensordatenverarbeitung und Auswertung"] },
          { date: "08/2022", place: "Rehab Zentrum Stadlau, Wien", title: "Praktikum im Bereich Forschung, Büro- und Laborassistenz" },
        ],
      },
      {
        id: "ehrenamt",
        title: "Ehrenamt",
        entries: [
          { date: "11/2026 – laufend", place: "Soli Deo Gloria Volleyball Vienna, Wien", title: "Mitgründer und Vorstandsmitglied (Verein in Gründung)", text: ["Mitwirkung am organisatorischen Aufbau des Vereins", "Entwicklung der Vereinsmanagement-Software sowie Gestaltung des visuellen Vereinsauftritts (Logo, Trikots und Corporate Design)"], project: "verein" },
          { date: "2023 – laufend", place: "Lokale Kirche, Wien", title: "Sound Engineering und Veranstaltungsplanung", text: ["Technische Betreuung von Veranstaltungen, Audiotechnik sowie Planung und Organisation von Veranstaltungen"], tech: "Live-Tontechnik, ProPresenter, Veranstaltungsplanung", techLabel: "Kompetenzen" },
          { date: "2019 – laufend", place: "Private Benefizveranstaltungen, Wien", title: "Mitorganisation und musikalische Mitwirkung", text: ["Gemeinsame Organisation und Durchführung jährlicher Benefiz-Weihnachtskonzerte mit meiner Familie (klassische Musik bis Jazz), musikalische Mitwirkung als Harfenist und Fagottist"] },
        ],
      },
      {
        id: "kenntnisse",
        title: "Kenntnisse",
        rows: [
          ["Programmiersprachen", "Java, JavaScript, TypeScript, Python, C#, SQL"],
          ["Frameworks", "Spring Boot, Svelte, Vue.js, Next.js, Tailwind CSS"],
          ["Plattformen und Tools", "Supabase, PostgreSQL, MongoDB, AWS S3, Docker, Git, GitLab CI/CD, Linux, Cypress"],
          ["Konzepte", "OOP, Algorithmen und Datenstrukturen, Datenbanken, Softwarearchitektur, Frontend- und Backendentwicklung"],
          ["Projektmanagement", "pma / IPMA Level D (pm basic), Projekt Management Austria"],
          ["Veranstaltungstechnik", "Live-Tontechnik, ProPresenter, Veranstaltungsplanung"],
          ["Sprachen", "Deutsch, Rumänisch (Muttersprache); Englisch, fließend in Wort und Schrift"],
        ],
      },
    ],
  },
  en: {
    lang: "en",
    cv: { label: "CV (PDF)", href: "uploads/CV.pdf" },
    landing: {
      who: "Studies software engineering at FH Wiener Neustadt and builds club software on an event bus of his own.",
      intro: "My largest project is software for clubs: members, calendar and tasks, built on an event bus library I wrote myself.",
      work: "Projects",
      cv: "Curriculum vitae",
      now: "present",
      music: { title: "Music", piece: "Fantasia", by: "Joe Hisaishi, from “Nausicaä of the Valley of the Wind”, played in 2023", text: "Besides programming I play the harp, since 2014 at the Vienna music schools, and the bassoon since 2018." },
    },
    ui: { technologies: "Technologies", prev: "Previous", next: "Next", console: "Console to try out", close: "Close", maximize: "Maximise", restore: "Restore", openPdf: "Diploma thesis (PDF)", source: "Source code", details: "Details", index: "Contents", back: "Back" },
    profile: {
      title: "Profile",
      summary: "Software engineering student with an HTL education in biomedical and health informatics. Experience in developing web applications and Java-based software, as well as in software architecture, databases and project management.",
      rows: [
        ["Interests", "Music (harp since 2014, bassoon since 2018, Vienna music schools), sports"],
      ],
    },
    sections: [
      { id: "projekte", title: "Projects", kind: "projects" },
      {
        id: "ausbildung",
        title: "Education",
        entries: [
          { date: "10/2025 – present", place: "FH Wiener Neustadt, Biotech Campus Tulln", title: "BSc Software Engineering und Systembau", tech: "Java, Spring Boot, JavaScript, Git, Linux, algorithms and data structures, databases, OOP" },
          { date: "2019 – 06/2024", place: "HTBLuVA Spengergasse, Vienna", title: "Specialisation in Biomedical and Health Informatics", text: ["Diploma thesis (written in English): Creating a Web Application for a Kenyan Women empowerment group selling their locally sourced products", "Personal responsibilities: Implementation/Development of the deployment, testing and quality control."], tech: "C#, Java, Python, JavaScript, SQL, Spring Boot, Git, project management, frontend and backend development", project: "eroots" },
        ],
      },
      {
        id: "erfahrung",
        title: "Experience",
        entries: [
          { date: "08/2024 – 02/2025", place: "Austrian Armed Forces, Hörsching & Vienna", title: "Basic military service" },
          { date: "08/2023", place: "Rehab Zentrum Stadlau, Vienna", title: "Internship in research and development", text: ["Development of an EEG device, sensor data processing and analysis"] },
          { date: "08/2022", place: "Rehab Zentrum Stadlau, Vienna", title: "Internship in research, office and laboratory assistance" },
        ],
      },
      {
        id: "ehrenamt",
        title: "Volunteer work",
        entries: [
          { date: "11/2026 – present", place: "Soli Deo Gloria Volleyball Vienna, Vienna", title: "Co-founder and board member (club in formation)", text: ["Helping to set up the organisation of the club", "Development of the club management software and design of the visual identity (logo, jerseys and corporate design)"], project: "verein" },
          { date: "2023 – present", place: "Local church, Vienna", title: "Sound engineering and event planning", text: ["Technical support at events, audio engineering, and planning and organisation of events"], tech: "live sound, ProPresenter, event planning", techLabel: "Skills" },
          { date: "2019 – present", place: "Private charity events, Vienna", title: "Co-organiser and musician", text: ["Organising and running annual charity Christmas concerts with my family (classical music to jazz); playing harp and bassoon"] },
        ],
      },
      {
        id: "kenntnisse",
        title: "Skills",
        rows: [
          ["Programming languages", "Java, JavaScript, TypeScript, Python, C#, SQL"],
          ["Frameworks", "Spring Boot, Svelte, Vue.js, Next.js, Tailwind CSS"],
          ["Platforms and tools", "Supabase, PostgreSQL, MongoDB, AWS S3, Docker, Git, GitLab CI/CD, Linux, Cypress"],
          ["Concepts", "OOP, algorithms and data structures, databases, software architecture, frontend and backend development"],
          ["Project management", "pma / IPMA Level D (pm basic), Projekt Management Austria"],
          ["Event technology", "live sound, ProPresenter, event planning"],
          ["Languages", "German, Romanian (native); English, fluent, written and spoken"],
        ],
      },
    ],
  },
};
