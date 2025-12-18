# TLS Certificate Automation Web Application

## Project Objective

The objective of this project is to create a **local, web-based TLS certificate automation tool** that allows users to easily generate, manage, and track self-signed TLS certificates for multiple domains. It follows a **GitOps-inspired workflow**, ensuring all certificate configurations are version-controlled and reproducible.

### Key Goals

1. **Simplify certificate creation:** Provide a user-friendly web interface where users can enter certificate details instead of manually editing YAML files.

2. **Automate certificate lifecycle:** Generate self-signed TLS certificates and automatically renew them when they are close to expiration.

3. **Maintain Git-based audit trail:** Commit all certificate configurations to a local Git repository to track changes, enable rollback, and maintain a versioned record of all certificates.

4. **Support multiple certificates:** Each domain has its own configuration and certificate folder, allowing management of multiple certificates simultaneously.

5. **Local, secure, and extensible:** Designed to run entirely on a local machine for development or internal use, with the potential to extend to remote Git repositories or production CA-signed certificates.

### Features

* Web form to enter TLS certificate details.
* Automatic YAML generation for each certificate.
* Git commit for every configuration change.
* TLS certificate creation and renewal based on configuration.
* Domain-based folder structure for organized certificate storage.
* Simple setup with Python, Flask, PyYAML, cryptography, and GitPython.

### Benefits

* Reduces manual errors and simplifies certificate management.
* Provides a clear version-controlled history of all certificates.
* Allows rapid creation and renewal of multiple TLS certificates.
* Serves as a foundation for a more advanced certificate management system.
