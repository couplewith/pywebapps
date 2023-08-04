/**
 * https://trufflesuite.com/docs/truffle/getting-started/using-the-truffle-dashboard/
 */


module.exports = {
// contracts_directory tells Truffle where the contracts you want to compile are located
   contracts_directory: './contracts',

// contracts_build_directory tells Truffle where to store compiled contracts
   contracts_build_directory: './build/local-contracts',

  networks: {
    // Useful for testing. The `development` name is special - truffle uses it by default
    //
     development: {
      host: "127.0.0.1",     // Localhost (default: none)
      port: 8545,            // Standard Ethereum port (default: none)
      network_id: "*",       // Any network (default: none)
     },
  },

  // Configure your compilers
  compilers: {
    solc: {
      version: "0.8.21",      // Fetch exact version from solc-bin (default: truffle's version)
    }
  },

};
