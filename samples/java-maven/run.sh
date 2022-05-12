docker run -it -v "$PWD":/app -v ~/.m2:/root/.m2 -w /app maven:3.8.4-openjdk-17-slim mvn test ci-speed:ci-speed

