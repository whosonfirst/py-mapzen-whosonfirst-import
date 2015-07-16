# py-mapzen-whosonfirst-importer

Import tools for the Who's On First

## Install

Depending on which version of rage-making Python or more likely the rage-making-er `setuptools` you are using you may need to expicitly tell the install script to put the command line tools in `/usr/local/bin` like this:

```
sudo python ./setup.py install --install-scripts /usr/local/bin
```

## Usage

_Please write me_

## Command line tools

### wof-importify

```
python scripts/wof-importify --dest /usr/local/mapzen/gazetteer-local/ --source custom --placetype minitenders --verbose ../minitenders/minitenders.geojson
```

## Known knowns

* For some reason simply listing Al's [address_normalizer](https://github.com/openvenues/address_normalizer) library in `setup.py` causes the install stuff to break. I have no idea...

## See also

