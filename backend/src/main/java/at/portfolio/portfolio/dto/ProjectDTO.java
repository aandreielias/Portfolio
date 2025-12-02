package at.portfolio.portfolio.dto;

import java.util.Map;

public class ProjectDTO {
    private String id;
    private String title;
    private String description;
    private String logo;
    private String cover;
    private String pdf;
    private Map<String, String> files; // Filename -> URL

    public ProjectDTO(String id, String title, String description, String logo, String cover, String pdf,
            Map<String, String> files) {
        this.id = id;
        this.title = title;
        this.description = description;
        this.logo = logo;
        this.cover = cover;
        this.pdf = pdf;
        this.files = files;
    }

    // Getters and Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getLogo() {
        return logo;
    }

    public void setLogo(String logo) {
        this.logo = logo;
    }

    public String getCover() {
        return cover;
    }

    public void setCover(String cover) {
        this.cover = cover;
    }

    public String getPdf() {
        return pdf;
    }

    public void setPdf(String pdf) {
        this.pdf = pdf;
    }

    public Map<String, String> getFiles() {
        return files;
    }

    public void setFiles(Map<String, String> files) {
        this.files = files;
    }
}
