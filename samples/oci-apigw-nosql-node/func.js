// Copyright (c) 2023 Oracle, Inc.  All rights reserved.
// Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
//

const fdk=require('@fnproject/fdk');
const process = require('process');
const NoSQLClient = require('oracle-nosqldb').NoSQLClient;
const Region = require('oracle-nosqldb').Region;
const ServiceType = require('oracle-nosqldb').ServiceType;
const url = require('url');

let client;
let lim = 15;

process.on('exit', function(code) {
  if (client) {
     console.log("\close client  on exit");
     client.close();
  }
  return code;
});

fdk.handle(async function(input, ctx){

  const apiKey=process.env.FN_API_KEY;
  const scopeRead ="read"
  const scopeWrite="write"
  let   apiKeyHeader;
  let   authScope = [];

  let tableName;
  let id;
  let descTable=false;

  // Reading parameters from standard input for TEST purposes
  // using invoke allows only to execute  getAllRecords
  if (input && input.tableName)
    tableName = input.tableName;
  if (input) {
    method = 'GET';
    apiKeyHeader = [apiKey]
    authScope = ["read", "write"]
  }


  // Reading parameters sent by the httpGateway
  // When an API Gateway is configured, you can execute all the defined actions
  let hctx = ctx.httpGateway
  if (hctx  && hctx.requestURL) {
        var adr = hctx.requestURL;
        var q = url.parse(adr, true);
        tableName = q.pathname.split('/')[2]
        id = q.pathname.split('/')[3]
        if (id && id === 'desc')
           descTable=true;
        method = hctx.method
        body = ctx.body
        apiKeyHeader = hctx.headers["X-Api-Key"]
        if (hctx.headers["X-Scope"]) 
           authScope.push(...hctx.headers["X-Scope"])    
  }

  // Validating apiKey - only if FN_API_KEY was configured at application/function level 
  if (apiKey) {
    if (! (apiKeyHeader)) {
      hctx.statusCode = 401
      return {"Api Key Validation":false, comment:"noApiKeyHeader"}
    }
    else if (! (apiKeyHeader.includes(apiKey))) {
      hctx.statusCode = 401
      return {"Api Key Validation":false, debug:apiKeyHeader}
    }
  }
  // Validating Scope if it was setup. 
  if (authScope) {
     if ( (! (authScope.includes(scopeRead)) ) && method==='GET'){
       hctx.statusCode = 401
       return {"Scope Validation":false, debug:authScope}
     }
     if ( (! (authScope.includes(scopeWrite)) ) && method!=='GET'){
       hctx.statusCode = 401
       return {"Scope Validation":false}
     }
  }

  // API Implementation
  
  if ( !client ) {
    client = createClientResource();
  }

  if ((method === 'GET') && !tableName){
    return showAll();
  }

  if ((method === 'GET') && descTable){
    return describeTable(tableName);
  }

  if ((method === 'GET') && id && !descTable){
    return getRecord(tableName, id);
  }

  if ((method === 'GET') && !id){
    return getAllRecords(tableName, q);
  }

  if ((method === 'POST') && !id){
    return createRecord(tableName, body);
  }

  if ((method === 'DELETE') ){
    return deleteRecord(tableName, id)
  }

  if ((method === 'PUT') && id ){
    return updateRecord (tableName, id,  body);
  }

  return showAll();
}, {});


// Show all tables

async function showAll () {

    try {
      let varListTablesResult = await client.listTables();
      return varListTablesResult;
    } catch (err){
        console.error('failed to show tables', err);
        return { error: err };
    } finally {
    }
}

// Show the structure of the table tablename

async function describeTable (tablename) {
   try {
      let resExistingTab = await client.getTable(tablename);
      await client.forCompletion(resExistingTab);
      return Object.assign(resExistingTab, { "schema": JSON.parse(resExistingTab.schema)});
   } catch (err){
        console.error('failed to show tables', err);
        return { error: err };
    } finally {
    }
}


// Create a new record in the table tablename
async function createRecord (tablename, record) {
    try {
        const result = await client.put(tablename, record, {exactMatch:true} );
        return { result: result};
    } catch (err) {
        console.error('failed to insert data', err);
        return { error: err };
    }
}

// Update a record in the table tablename
async function updateRecord (tablename, id,  record) {
    try {
        const result = await client.putIfPresent(tablename, Object.assign(record, {id}) );
        return { result: result};
    } catch (err) {
        console.error('failed to insert data', err);
        return { error: err };
    }
}

// Get a record from the table tablename by id
// Currently the id is hardcoded as key of the table
async function getRecord (tablename, id) {
    try {
        const result = await client.get(tablename, { id })
        if (result.row)
          return result.row;
        else
          return {}
    } catch (err) {
        console.error('failed to get data', err);
        return { error: err };
    }
}

// Delete a record from the table tablename by id
// Currently the id is hardcoded as key of the table
async function deleteRecord (tablename, id) {
    try {
        const result = await client.delete(tablename, { id });
        return { result: result};
    } catch (err) {
        console.error('failed to delete data', err);
        return { error: err };
    }
}

// Get all records for the table tablename
async function getAllRecords (tablename, req) {
    let statement = "SELECT * FROM " + tablename;
    let offset;
    let page;
    let limit;
    let orderby;
    let result;

    if (req && req.query ) {
      page = parseInt(req.query.page);
      limit = parseInt(req.query.limit);
      orderby = req.query.orderby;
    }

    if (orderby )
      statement = statement + " ORDER BY " + orderby;
    if (limit)
      statement = statement + " LIMIT " + limit;
    if (page && limit) {
      offset = page*limit;
      statement = statement + " OFFSET " + offset;
    }

    console.log (statement)
    result =executeQuery (statement)
    if (result)
      return result;
    else
      return {}

}

async function executeQuery (statement) {
  const rows = [];
  let cnt ;
  let res;
  try {
    do {
       res = await client.query(statement, { continuationKey:cnt});
       rows.push.apply(rows, res.rows);
       cnt = res.continuationKey;
    } while(res.continuationKey != null);
  }
  catch(err) {
        return err;
  }
  return rows;
}

function createClientResource() {
  return  new NoSQLClient({
    region: process.env.NOSQL_REGION,
    compartment:process.env.NOSQL_COMPARTMENT_ID,
    auth: {
        iam: {
            useResourcePrincipal: true
        }
    }
  });
}
