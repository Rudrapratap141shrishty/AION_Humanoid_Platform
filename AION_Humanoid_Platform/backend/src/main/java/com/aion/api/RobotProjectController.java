package com.aion.api;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/robots")
public class RobotProjectController {
    private final RobotProjectRepository repository;

    public RobotProjectController(RobotProjectRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<RobotProject> all(@RequestParam(required = false) String category) {
        return (category == null || category.isBlank())
                ? repository.findAll()
                : repository.findByCategoryIgnoreCase(category);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public RobotProject create(@Valid @RequestBody RobotProject project) {
        return repository.save(project);
    }

    @GetMapping("/{id}")
    public RobotProject one(@PathVariable Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new RobotNotFoundException(id));
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        if (!repository.existsById(id)) throw new RobotNotFoundException(id);
        repository.deleteById(id);
    }
}
