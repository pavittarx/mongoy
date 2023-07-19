A wrapper library on top of pymongo.

```shell
  pip install mongoy
```

## Connecting to Database

```python
   from mongoy.mongo import Mongo

   connection = 'mongodb://127.0.0.1:27017'
   db_name = 'mydb''

   mgy = Mongo(connection, db_name)
```


### Get `pymongo` db instance
```python
  # get pymongo db instance
  db = mgy.get_db()
```

### Register a collection for operations

```python
   # Register a collection for CRUD data ops

   mgy.register_collection('users')
```

```python
  # Add a document
  doc = {
    'name': 'test',
    'age': 10,
  }

  result = mgy.users.insert(doc)


  # Add multiple documents
  docs = [{
    'name': 'testuser',
    'age': 21
  }, {
    'name': 'testy',
    'age': 22
  }, {
    'name': 'uwoo',
    'age': 27
  }]

  result = mgy.users.insert(docs)
```

```python
  # Find Documents

  result = mgy.users.find()

  age_22_users = mgy.users.find({
    'age': 22
  })

  others = mgy.users.find({
    'age': {'$ne': 22}
  })

  mgy.users.find({
    '_id': result[0]['_id']
  })
```

```python
  from bson.objectid import ObjectId
  id = ObjectId('some-mongo-id')

  # Update single document 
  mgy.users.find_one_and_update({'_id': id}, {'$set': {'age': 30}})

  # Update all matching documents
  mgy.users.find_all_and_update({'age': {'$lt': 25}}, {'$set': {'age': 30}})

  # Insert if not exists 
  mgy.users.find_one_and_update({'_id': id}, {'$set': {'age': 30}}, upsert=True)
```

```python
  # Delete Single Documents
  mgy.users.delete({
    'age': 22
  })

   # Delete all matching Documents
  mgy.users.delete({
    'age': 22
  }, all=True)

```