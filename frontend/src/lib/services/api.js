// Use Vite's base URL for correct path resolving on GitHub Pages
const BASE_URL = import.meta.env.BASE_URL;

export class ApiService {
    static async fetchAllTechs() {
        try {
            const response = await fetch(`${BASE_URL}data/tech.json`);
            if (!response.ok) throw new Error("Failed to fetch techs");
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("ApiService Error:", error);
            return [];
        }
    }

    static async fetchTech(id) {
        try {
            const allTechs = await this.fetchAllTechs();
            return allTechs.find(t => t.id === id) || null;
        } catch (error) {
            console.error("ApiService Error:", error);
            return null;
        }
    }

    static async fetchAllProjects() {
        try {
            const response = await fetch(`${BASE_URL}data/project.json`);
            if (!response.ok) throw new Error("Failed to fetch projects");
            return await response.json();
        } catch (error) {
            console.error("ApiService Error:", error);
            return [];
        }
    }

    static async fetchProject(id) {
        try {
            const allProjects = await this.fetchAllProjects();
            return allProjects.find(p => p.id === id) || null;
        } catch (error) {
            console.error("ApiService Error:", error);
            return null;
        }
    }
}
