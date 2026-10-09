package com.aion.api;

import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface RobotProjectRepository extends JpaRepository<RobotProject, Long> {
    List<RobotProject> findByCategoryIgnoreCase(String category);
}
