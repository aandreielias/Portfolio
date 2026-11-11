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
      { src: "uploads/projects/Vereinsmanagement/kalender.png", de: "Kalender mit Trainings, Sitzungen, Turnieren und Fristen", en: "Calendar with training sessions, meetings, tournaments and deadlines" },
      { src: "uploads/projects/Vereinsmanagement/aufgaben.png", de: "Aufgaben mit Fälligkeit, Zuständigen und Checklisten", en: "Tasks with due dates, assignees and checklists" },
      { src: "uploads/projects/Vereinsmanagement/mitglieder.png", de: "Mitgliederverwaltung mit Rollen", en: "Member management with roles" },
    ],
    de: {
      title: "Vereinsmanagement-Software",
      summary: "Webanwendung (Front- & Backend) zur Verwaltung von Mitgliedern, Terminen, Aufgaben, Aktivitäten, Sitzungen, Dateien und integrierten E-Mails",
      body: [
        "Entwicklung für Soli Deo Gloria Volleyball Vienna, einen Verein in Gründung, den ich mitgegründet habe. Vereinsspezifische Angaben wie Name, Rollen und Mitgliedsarten sind Einstellungen, damit die Software auch für andere Vereine nutzbar ist.",
        "Backend als modularer Monolith in Spring Boot mit 13 Fachmodulen, darunter Mitglieder, Teams, Kalender, Sitzungen, Aufgaben, Dateien, Inventar und Turniere. Die Module kommunizieren ausschließlich über meine Event-Bus-Bibliothek; die Schichtgrenzen werden mit ArchUnit-Tests geprüft.",
        "Datenhaltung in PostgreSQL (Supabase) mit 145 Flyway-Migrationen und Row-Level-Security auf jeder Tabelle. Aus der OpenAPI-Spezifikation des Servers werden die TypeScript-Typen des Frontends generiert, Änderungen erscheinen über WebSocket sofort bei allen Nutzern.",
        "Frontend in Svelte 5 und TypeScript ohne UI-Framework. Ein Demo-Modus bildet die gesamte API im Browser nach; die Abbildungen zeigen diesen Modus mit Testdaten.",
      ],
    },
    en: {
      title: "Club management software",
      summary: "Web application (frontend & backend) for managing members, appointments, tasks, activities, meetings, files and integrated email",
      body: [
        "Built for Soli Deo Gloria Volleyball Vienna, a club in formation that I co-founded. Club-specific details such as name, roles and membership types are settings, so other clubs can use the software as well.",
        "Backend as a modular monolith in Spring Boot with 13 domain modules, among them members, teams, calendar, meetings, tasks, files, inventory and tournaments. The modules communicate only through my event bus library; ArchUnit tests check the layer boundaries.",
        "Data stored in PostgreSQL (Supabase) with 145 Flyway migrations and row-level security on every table. The frontend's TypeScript types are generated from the server's OpenAPI specification, and changes reach all users at once over WebSocket.",
        "Frontend in Svelte 5 and TypeScript without a UI framework. A demo mode runs the whole API in the browser; the screenshots show this mode with test data.",
      ],
    },
  },
  {
    id: "eventbus",
    year: "2026",
    tech: "Java, Maven, JUnit, Git",
    link: "https://github.com/aandreielias/EventBus",
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
        "Publish/Subscribe-Bibliothek für Java 21 ohne Laufzeitabhängigkeiten. Bestandteil der Backend-Kernarchitektur der Vereinsmanagement-Software, in der alle Module über den Bus kommunizieren.",
        "Funktionen: hierarchisches Routing über Kanalpfade, Prioritäten, asynchrone Zustellung auf virtuellen Threads mit Obergrenze, Request/Response mit Timeouts, Dead-Letter-Handler und schwache Referenzen auf Subscriber.",
        "Das Kommandozeilenwerkzeug ebus verbindet sich über JMX mit einer laufenden Anwendung und zeigt Kanäle, Subscriber und Zustellstatistiken an.",
      ],
    },
    en: {
      title: "Event bus library",
      summary: "Independent development of a lightweight Java library for asynchronous event communication and messaging",
      body: [
        "Publish/subscribe library for Java 21 with no runtime dependencies. Part of the core backend architecture of the club management software, where all modules communicate through the bus.",
        "Features: hierarchical routing by channel path, priorities, asynchronous delivery on virtual threads with a cap, request/response with timeouts, a dead-letter handler and weak references to subscribers.",
        "The command-line tool ebus attaches to a running application over JMX and shows channels, subscribers and delivery statistics.",
      ],
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
      summary: "Persönliche Website mit Lebenslauf und Projekten, gestaltet nach dem Layout des Lebenslaufs",
      body: [
        "Statische Single-Page-Anwendung mit Svelte 5 und Vite, die über GitHub Actions auf GitHub Pages veröffentlicht wird.",
        "Alle Inhalte liegen auf Deutsch und Englisch in einer Datei. Projekte öffnen sich als verschiebbare, skalierbare Fenster, Abbildungen in einer Zoom-Ansicht.",
        "Version 4 (November 2026): Neugestaltung und Neuaufbau mit weniger Komponenten und ohne ungenutzte Abhängigkeiten.",
      ],
    },
    en: {
      title: "Portfolio website",
      summary: "Personal website with CV and projects, designed after the layout of the CV",
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
    ui: { technologies: "Technologien", close: "Schließen", maximize: "Maximieren", restore: "Verkleinern", openPdf: "Diplomarbeit (PDF)", source: "Quellcode", details: "Details", index: "Inhalt", back: "Zurück" },
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
          { date: "2025 – laufend", place: "FH Wiener Neustadt, Biotech Campus Tulln", title: "BSc Software Engineering und Systembau", tech: "Java, Spring Boot, JavaScript, Git, Linux, Algorithmen und Datenstrukturen, Datenbanken, OOP" },
          { date: "2019 – 2024", place: "HTBLuVA Spengergasse, Wien", title: "Ausbildungsschwerpunkt Biomedizin und Gesundheitsinformatik", text: ["Diplomarbeit (in englischer Sprache): Creating a Web Application for a Kenyan Women empowerment group selling their locally sourced products", "Persönlicher Aufgabenbereich: Implementation/Development of the deployment, testing and quality control."], tech: "C#, Java, Python, JavaScript, SQL, Spring Boot, Git, Projektmanagement, Frontend- und Backendentwicklung", project: "eroots" },
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
      { id: "kontakt", title: "Kontakt", kind: "contact" },
    ],
  },
  en: {
    lang: "en",
    cv: { label: "CV (PDF)", href: "uploads/CV.pdf" },
    ui: { technologies: "Technologies", close: "Close", maximize: "Maximise", restore: "Restore", openPdf: "Diploma thesis (PDF)", source: "Source code", details: "Details", index: "Contents", back: "Back" },
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
          { date: "2025 – present", place: "FH Wiener Neustadt, Biotech Campus Tulln", title: "BSc Software Engineering und Systembau", tech: "Java, Spring Boot, JavaScript, Git, Linux, algorithms and data structures, databases, OOP" },
          { date: "2019 – 2024", place: "HTBLuVA Spengergasse, Vienna", title: "Specialisation in Biomedical and Health Informatics", text: ["Diploma thesis (written in English): Creating a Web Application for a Kenyan Women empowerment group selling their locally sourced products", "Personal responsibilities: Implementation/Development of the deployment, testing and quality control."], tech: "C#, Java, Python, JavaScript, SQL, Spring Boot, Git, project management, frontend and backend development", project: "eroots" },
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
      { id: "kontakt", title: "Contact", kind: "contact" },
    ],
  },
};
