const mongoose = require('mongoose');

const EmployeeEmailSchema = new mongoose.Schema({
  value: { type: String, required: true },
  position: { type: String }
}, { _id: false });

const EmployeeSchema = new mongoose.Schema({
  domain: { type: String, required: true },
  emails: [EmployeeEmailSchema]
}, { _id: false });

const TechnologySchema = new mongoose.Schema({
  domain: { type: String, required: true },
  technologies: { type: mongoose.Schema.Types.Mixed } // flexible JSON
}, { _id: false });

const AttackSurfaceSchema = new mongoose.Schema({
  domains: [{
    domain: { type: String, required: true },
    ips: [String]
  }],
  ips: [{
    ip: { type: String, required: true },
    org: String,
    loc: String
  }]
}, { _id: false });

const ObjectSchema = new mongoose.Schema({
  domain: { type: String, required: true },
  attack_surface: AttackSurfaceSchema,
  technologies: TechnologySchema,
  employees: EmployeeSchema
}, { timestamps: true });


const StoredObject = mongoose.model('StoredObject', ObjectSchema);
module.exports = StoredObject;
