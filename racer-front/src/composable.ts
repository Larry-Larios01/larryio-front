import { useNetwork } from '@vueuse/core'
import {CompetitionClientFetch, CompetitionClientPg} from '@/client'


const maria = useNetwork()


export async function useClient(){

    const network = useNetwork()
    if(network.isOnline.value){
        const connection =  new CompetitionClientFetch(); 
        return connection

    }

    if(!network.isOnline.value){
        const connection =  new CompetitionClientPg()
        return connection

    }
    
    


}