package at.portfolio.portfolio.dto;

import java.util.Map;

public class TechShowcaseDTO {
    private String id;
    private String title;
    private String language;
    private String description;
    private Map<String, String> files;

    public TechShowcaseDTO(String id, String title, String language, String description, Map<String, String> files) {
        this.id = id;
        this.title = title;
        this.language = language;
        this.description = description;
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

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Map<String, String> getFiles() {
        return files;
    }

    public void setFiles(Map<String, String> files) {
        this.files = files;
    }
}
