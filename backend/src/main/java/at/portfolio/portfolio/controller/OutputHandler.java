package at.portfolio.portfolio.controller;

import at.portfolio.portfolio.dto.ProjectDTO;
import at.portfolio.portfolio.dto.TechShowcaseDTO;
import at.portfolio.portfolio.service.ProjectRegistry;
import at.portfolio.portfolio.service.TechRegistry;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.MalformedURLException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

@RestController
@RequestMapping("/api")
@CrossOrigin(origins = "*")
public class OutputHandler {

    private final TechRegistry techRegistry;
    private final ProjectRegistry projectRegistry;
    private final Path projectDir = Paths.get("uploads/projects");

    public OutputHandler(TechRegistry techRegistry, ProjectRegistry projectRegistry) {
        this.techRegistry = techRegistry;
        this.projectRegistry = projectRegistry;
    }

    // --- Tech Endpoints ---

    @GetMapping("/tech")
    public ResponseEntity<List<TechShowcaseDTO>> getAllTechs() {
        return ResponseEntity.ok(techRegistry.getAllTechShowcases());
    }

    @GetMapping("/tech/{id}")
    public ResponseEntity<TechShowcaseDTO> getTech(@PathVariable String id) {
        TechShowcaseDTO tech = techRegistry.getTechShowcase(id);
        if (tech != null) {
            return ResponseEntity.ok(tech);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    // --- Project Endpoints ---

    @GetMapping("/project")
    public ResponseEntity<List<ProjectDTO>> getAllProjects() {
        return ResponseEntity.ok(projectRegistry.getAllProjects());
    }

    @GetMapping("/project/{id}")
    public ResponseEntity<ProjectDTO> getProject(@PathVariable String id) {
        ProjectDTO project = projectRegistry.getProject(id);
        if (project != null) {
            return ResponseEntity.ok(project);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/project/{id}/file/{filename}")
    public ResponseEntity<Resource> getProjectFile(@PathVariable String id, @PathVariable String filename) {
        try {
            Path file = projectDir.resolve(id).resolve(filename);
            Resource resource = new UrlResource(file.toUri());

            if (resource.exists() || resource.isReadable()) {
                // Determine content type
                MediaType mediaType = MediaType.APPLICATION_OCTET_STREAM;
                String lowerName = filename.toLowerCase();
                if (lowerName.endsWith(".pdf")) {
                    mediaType = MediaType.APPLICATION_PDF;
                } else if (lowerName.endsWith(".png")) {
                    mediaType = MediaType.IMAGE_PNG;
                } else if (lowerName.endsWith(".jpg") || lowerName.endsWith(".jpeg")) {
                    mediaType = MediaType.IMAGE_JPEG;
                }

                return ResponseEntity.ok()
                        .contentType(mediaType)
                        .body(resource);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (MalformedURLException e) {
            return ResponseEntity.badRequest().build();
        }
    }

    @GetMapping("/self")
    public ResponseEntity<Resource> getProfileImage() {
        try {
            Path file = Paths.get("uploads/self.jpeg");
            Resource resource = new UrlResource(file.toUri());

            if (resource.exists() || resource.isReadable()) {
                return ResponseEntity.ok()
                        .contentType(MediaType.IMAGE_JPEG)
                        .body(resource);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (MalformedURLException e) {
            return ResponseEntity.badRequest().build();
        }
    }
}
