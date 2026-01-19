# 🛠️ Real Estate Project - Database Schema

Generated from the project's Django models to provide a clear overview of the data structure.

---

## 👤 Users App

### `CustomUser`

The custom user model extending Django's default `AbstractUser`.

| Field         | Type          | Description                                                           |
| :------------ | :------------ | :-------------------------------------------------------------------- |
| `id`          | BigAutoField  | Primary Key.                                                          |
| `username`    | CharField     | Unique username for identifies users.                                 |
| `email`       | EmailField    | User email address.                                                   |
| `image`       | ImageField    | Profile picture. Path: `images/users`. Default: `images/account.jpg`. |
| `location`    | PointField    | Geographic location coordinates (GIS).                                |
| `is_staff`    | BooleanField  | Designates whether the user can log into this admin site.             |
| `is_active`   | BooleanField  | Designates whether this user should be treated as active.             |
| `date_joined` | DateTimeField | Date and time when the account was created.                           |

---

## 🏠 Base App

### `Estate`

The core entity representing a property listing.

| Field           | Type            | Description                                         |
| :-------------- | :-------------- | :-------------------------------------------------- |
| `id`            | BigAutoField    | Primary Key.                                        |
| `owner`         | ForeignKey      | Link to `CustomUser` (Owner of the estate).         |
| `address`       | ForeignKey      | Link to `Address` object.                           |
| `description`   | TextField       | Full description of the property.                   |
| `space`         | IntegerField    | Area/Space of the building or land.                 |
| `coordinates`   | PointField      | GIS point coordinates for map placement.            |
| `offers`        | ManyToManyField | Relationship to the `Offer` model.                  |
| `deadline`      | DateField       | The date by which the estate listing ends.          |
| `created`       | DateField       | Date when the estate was listed (auto-added).       |
| `property_type` | CharField       | Type of property. Choices: `Shop`, `House`, `Land`. |
| `price`         | IntegerField    | Asking price for the property.                      |
| `active`        | BooleanField    | Status of the listing (Visible/Hidden).             |

### `Offer`

Represents financial offers made by users on specific estates.

| Field     | Type          | Description                                  |
| :-------- | :------------ | :------------------------------------------- |
| `id`      | BigAutoField  | Primary Key.                                 |
| `user`    | ForeignKey    | Link to the `CustomUser` who made the offer. |
| `price`   | IntegerField  | The monetary value of the offer.             |
| `created` | DateTimeField | Timestamp of when the offer was submitted.   |

### `Address`

Structured location data for estates.

| Field          | Type          | Description                            |
| :------------- | :------------ | :------------------------------------- |
| `id`           | BigAutoField  | Primary Key.                           |
| `country`      | CharField(30) | Country where the estate is located.   |
| `governate`    | CharField(20) | Governorate or state.                  |
| `area`         | CharField(30) | Specific area or district.             |
| `neighborhood` | CharField(40) | Neighborhood name.                     |
| `building_no`  | CharField     | Identification number of the building. |

---

_Last Updated: 2026-01-15_
