package at.portfolio.portfolio.service;

import at.portfolio.portfolio.dto.ProjectDTO;
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
public class ProjectRegistry {

    private final Path projectDir = Paths.get("uploads/projects");

    public List<ProjectDTO> getAllProjects() {
        List<ProjectDTO> projects = new ArrayList<>();
        if (!Files.exists(projectDir))
            return projects;

        try (Stream<Path> paths = Files.list(projectDir)) {
            paths.filter(Files::isDirectory).forEach(dir -> {
                String id = dir.getFileName().toString();
                String title = id;
                String description = "Project description placeholder.";

                if (id.equalsIgnoreCase("ERoots")) {
                    description = "Work in Progress";
                } else if (id.equalsIgnoreCase("Portfolio")) {
                    title = "Portfolio Website";
                    description = "A modern, responsive portfolio website built with Svelte and Spring Boot.";
                }

                Map<String, String> files = new HashMap<>();

                // Use array wrappers to allow modification in lambda
                final String[] logo = { null };
                final String[] cover = { null };
                final String[] pdf = { null };

                try (Stream<Path> filePaths = Files.list(dir)) {
                    filePaths.filter(Files::isRegularFile).forEach(file -> {
                        String fileName = file.getFileName().toString();
                        String fileUrl = "/api/project/" + id + "/file/" + fileName;
                        files.put(fileName, fileUrl);

                        if (fileName.toLowerCase().endsWith(".pdf")) {
                            pdf[0] = fileUrl;
                        } else if (fileName.equalsIgnoreCase("logo.png") || fileName.equalsIgnoreCase("logo.svg")) {
                            logo[0] = fileUrl;
                        } else if (fileName.equalsIgnoreCase("landing.png") || fileName.equalsIgnoreCase("cover.png")) {
                            cover[0] = fileUrl;
                        }
                    });
                } catch (IOException e) {
                    e.printStackTrace();
                }

                projects.add(new ProjectDTO(id, title, description, logo[0], cover[0], pdf[0], files));
            });
        } catch (IOException e) {
            e.printStackTrace();
        }
        return projects;
    }

    public ProjectDTO getProject(String id) {
        return getAllProjects().stream()
                .filter(p -> p.getId().equals(id))
                .findFirst()
                .orElse(null);
    }
}
