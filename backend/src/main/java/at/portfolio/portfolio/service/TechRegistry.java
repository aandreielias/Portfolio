package at.portfolio.portfolio.service;

import at.portfolio.portfolio.dto.TechShowcaseDTO;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Stream;

@Service
public class TechRegistry {

    private final Path techDir = Paths.get("uploads/tech");

    public List<TechShowcaseDTO> getAllTechShowcases() {
        List<TechShowcaseDTO> showcases = new ArrayList<>();
        if (!Files.exists(techDir))
            return showcases;

        try (Stream<Path> paths = Files.list(techDir)) {
            paths.filter(Files::isDirectory).forEach(dir -> {
                String id = dir.getFileName().toString();
                String title = id; // Default title is folder name
                String description = "No description available.";
                Map<String, String> files = new HashMap<>();

                try (Stream<Path> filePaths = Files.walk(dir)) {
                    filePaths.filter(Files::isRegularFile).forEach(file -> {
                        String fileName = file.getFileName().toString();
                        try {
                            if (!fileName.startsWith(".")) {
                                String content = Files.readString(file);
                                files.put(fileName, content);
                            }
                        } catch (IOException e) {
                            System.err.println("Error reading file: " + fileName);
                        }
                    });
                } catch (IOException e) {
                    e.printStackTrace();
                }

                // Determine language after collecting files
                String language = "unknown";
                if (files.keySet().stream().anyMatch(f -> f.endsWith(".py")))
                    language = "python";
                else if (files.keySet().stream().anyMatch(f -> f.endsWith(".java")))
                    language = "java";
                else if (files.keySet().stream().anyMatch(f -> f.endsWith(".js")))
                    language = "javascript";

                if (files.containsKey("simulator.py") || id.equalsIgnoreCase("DashboardSim")
                        || id.toLowerCase().contains("sim")) {
                    description = "A high-fidelity Python simulation of a 2005 VW Phaeton W12 LWB. This project models the complex interaction between the 6.0L W12 engine, ZF 5HP24A automatic transmission, and the vehicle's chassis dynamics. It includes a real-time thermodynamic system, fluid dynamics for the torque converter, and a fully functional digital dashboard interface built with Tkinter.";
                }

                showcases.add(new TechShowcaseDTO(id, title, language, description, files));
            });
        } catch (IOException e) {
            e.printStackTrace();
        }
        return showcases;
    }

    public TechShowcaseDTO getTechShowcase(String id) {
        return getAllTechShowcases().stream()
                .filter(t -> t.getId().equals(id))
                .findFirst()
                .orElse(null);
    }
}
