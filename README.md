# INVENTARIO
#### Video Demo:  https://www.youtube.com/watch?v=5aS0oOh3_hk
#### Description:

# Project Description

The aim of this project is to address an emerging issue in a chemical company that manufactures food substitutes. There's a recognized need to create a detailed inventory of all the equipment and components used in the production plant.

The plant comprises 15 production areas, each housing an average of 20 pieces of equipment. Each piece of equipment, in turn, utilizes an average of 5 components.

This program seeks to provide a structure for collecting information corresponding to each component, equipment, and area, thereby facilitating access to it.

### Databases

The program consists of three main databases:

1. **Areas**
2. **Equipment**
3. **Components**

Each of these databases contains various variables to accurately identify each item, including:

- Name
- Location
- Area
- Equipment
- Component
- Tag
- Brand
- Model
- Description
- Type
- Image to visualize the equipment (JPG format)
- Corresponding safety/operation manual (PDF format)
- Maintenance execution dates
- Parts/maintenance provider

### Program Features

The program offers various functionalities organized into different sections:

- **All Areas**
- **All Equipment**
- **All Components**
- **Equipment by Area**
- **Components by Equipment**
- **Area Creation**
- **Equipment Creation**
- **Component Creation**
- **Area Editing**
- **Equipment Editing**
- **Component Editing**
- **Area Deletion**
- **Equipment Deletion**
- **Component Deletion**
- **File Upload (JPG or PDF) on Equipment and Components**
- **Login**
- **User Registration**
- **Logout**

### Implementation and Routing

The project was based on the "finance" project's code, although significant modifications were made to routing and overall functionality. The program handles all transactions using different routes, including:

- `/`
- `/new_area`
- `/areas`
- `/edit_area`
- `/delete_area`
- `/new_equipment`
- `/equipment`
- `/edit_equipment`
- `/delete_equipment`
- `/new_component`
- `/edit_component`
- `/delete_component`
- `/all_components`
- `/all_equipment`
- `/login`
- `/register`
- `/logout`
- `/uploads/<name>`

### User Interface

The project includes a series of HTML files that provide a user interface for various actions:

- `areas.html`: Displays the registered areas in the plant with options to create, edit, and delete.
- `edit_area.html`, `edit_equipment.html`, `edit_component.html`: Displays information contained in a specific area, equipment, or component, with the option to modify and update it in the database.
- `all_components.html`, `all_equipment.html`: Displays all existing components or equipment with options to edit or delete.
- `components.html`, `equipment.html`: Displays components or equipment related to a particular equipment or area, with options to create, edit, or delete components.
- `new_area.html`, `new_equipment.html`, `new_component.html`: Presents a form for creating an area, equipment, or component, facilitating its registration in the database.

This program, implemented in Python, manages all transactions through the aforementioned routes, providing a comprehensive solution for controlling and managing assets in the chemical plant.
