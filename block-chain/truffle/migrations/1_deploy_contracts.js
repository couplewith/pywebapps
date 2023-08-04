//const SimpleStorage = artifacts.require("SimpleStorage");
//const SimpleStorage = artifacts.require("SimpleStorage");
var SimpleStorage = artifacts.require("SimpleStorage");

module.exports = function(deployer) {
  deployer.deploy(SimpleStorage);
};

