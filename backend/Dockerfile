# Build Stage
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app

# Copy pom.xml and download dependencies
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy source code and build
COPY src ./src
RUN mvn clean package -DskipTests -B

# Run Stage
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

# Copy the built artifact
COPY --from=build /app/target/*.jar app.jar

# Copy the uploads directory to the container
COPY uploads ./uploads

EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
