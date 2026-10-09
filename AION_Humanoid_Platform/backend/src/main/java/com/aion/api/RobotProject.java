package com.aion.api;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import java.time.Instant;

@Entity
@Table(name = "robot_projects", indexes = {
    @Index(name = "idx_robot_category", columnList = "category")
})
public class RobotProject {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    @Column(nullable = false, length = 120)
    private String name;

    @Column(nullable = false, length = 40)
    private String category = "humanoid";

    @Column(length = 1000)
    private String description;

    @Column(nullable = false, updatable = false)
    private Instant createdAt = Instant.now();

    public RobotProject() {}
    public RobotProject(String name, String category, String description) {
        this.name = name;
        this.category = (category == null || category.isBlank()) ? "humanoid" : category;
        this.description = description;
    }
    public Long getId() { return id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    public Instant getCreatedAt() { return createdAt; }
}
