from Box2D.examples.framework import Keys
from managers.EntityManager import EntityManager
from managers.NetworkManager import NetworkManager
from serverEntities.ServerEntity import ServerEntity


class PlayerManager(object):
    """
    Attributes:
        idx_dict: Stores id of objects. Looks like {id(obj): obj, }
        addr_dict: Stores ids of a port can control. Looks like {str: set(id(obj), ), }
        pressed_keys: Debug only.
    """

    def __init__(self, entity_manager: EntityManager, network_manager: NetworkManager):
        self.entity_manager = entity_manager
        self.network_manager = network_manager
        self.idx_dict = {}
        self.addr_dict = {}
        self.pressed_keys = set()

    def bindPlayer(self, entity: ServerEntity, addr):
        if addr not in self.addr_dict:
            self.addr_dict[addr] = set()
            self.network_manager.bindPort(addr)
        self.addr_dict[addr].add(id(entity))
        self.idx_dict[id(entity)] = entity
        entity.owner = addr

    def debugBindPlayer(self, entity: ServerEntity):
        """
        Set a player controlled with the keyboard on server.
        Args:
            entity: Literally.
        """
        if 'debugInput' not in self.addr_dict:
            self.addr_dict['debugInput'] = set()
        self.addr_dict['debugInput'].add(id(entity))
        self.idx_dict[id(entity)] = entity
        entity.owner = 'debugInput'

    def unbindPlayer(self, idx):
        #TODO: need a inverted index but 04119 is lazy
        print(idx)
        for p in self.addr_dict:
            d = self.addr_dict[p]
            if idx in d:
                self.idx_dict[idx] = None
                d.remove(idx)
                print(str(idx)+'at'+str(d)+'unbound')

    def pushEvent(self, port, d):
        try:
            if 'idx' in d:
                if port in self.addr_dict:
                    pd = self.addr_dict[port]
                    if d['idx'] in pd:
                        entity = self.idx_dict[d['idx']]
                        entity.setInput(d)
        except Exception as e:
            print(e)

    def debugKeyDown(self, key):
        self.pressed_keys.add(key)
        self.debugKeyEvent(key, True)

    def debugKeyUp(self, key):
        self.pressed_keys.discard(key)
        self.debugKeyEvent(key, False)

    def debugKeyEvent(self, key, pressed):
        if 'debugInput' in self.addr_dict:
            for i in self.addr_dict['debugInput']:
                entity = self.idx_dict[i]
                if Keys.K_w in self.pressed_keys:
                    entity.setInput({'accY': 1})
                elif Keys.K_s in self.pressed_keys:
                    entity.setInput({'accY': -1})
                else:
                    entity.setInput({'accY': 0})

                if Keys.K_e in self.pressed_keys:
                    entity.setInput({'accX': 1})
                elif Keys.K_q in self.pressed_keys:
                    entity.setInput({'accX': -1})
                else:
                    entity.setInput({'accX': 0})

                if Keys.K_a in self.pressed_keys:
                    entity.setInput({'accR': 1})
                elif Keys.K_d in self.pressed_keys:
                    entity.setInput({'accR': -1})
                else:
                    entity.setInput({'accR': 0})

                if Keys.K_j in self.pressed_keys:
                    entity.setInput({'fire': 1})
                else:
                    entity.setInput({'fire': 0})

    def update(self):
        for d in self.network_manager.dataRead():
            if len(d) >= 3:
                self.pushEvent(d[0], d[2][1])
