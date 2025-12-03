const API_BASE = import.meta.env.VITE_API_URL || "/api";

export class ApiService {
    static async fetchAllTechs() {
        try {
            const response = await fetch(`${API_BASE}/tech`);
            if (!response.ok) throw new Error("Failed to fetch techs");
            const data = await response.json();
            return data.map(tech => {
                if (tech.id === "DashboardSim" && tech.description === "No description available.") {
                    return {
                        ...tech,
                        description: "A high-fidelity Python simulation of a 2005 VW Phaeton W12 LWB. This project models the complex interaction between the 6.0L W12 engine, ZF 5HP24A automatic transmission, and the vehicle's chassis dynamics. It includes a real-time thermodynamic system, fluid dynamics for the torque converter, and a fully functional digital dashboard interface built with Tkinter."
                    };
                }
                return tech;
            });
        } catch (error) {
            console.error("InputHandler Error:", error);
            return [];
        }
    }

    static async fetchTech(id) {
        try {
            const response = await fetch(`${API_BASE}/tech/${id}`);
            if (!response.ok) throw new Error("Failed to fetch tech");
            return await response.json();
        } catch (error) {
            console.error("InputHandler Error:", error);
            return null;
        }
    }

    static async fetchAllProjects() {
        try {
            const response = await fetch(`${API_BASE}/project`);
            if (!response.ok) throw new Error("Failed to fetch projects");
            return await response.json();
        } catch (error) {
            console.error("InputHandler Error:", error);
            return [];
        }
    }

    static async fetchProject(id) {
        try {
            const response = await fetch(`${API_BASE}/project/${id}`);
            if (!response.ok) throw new Error("Failed to fetch project");
            return await response.json();
        } catch (error) {
            console.error("InputHandler Error:", error);
            return null;
        }
    }
}
