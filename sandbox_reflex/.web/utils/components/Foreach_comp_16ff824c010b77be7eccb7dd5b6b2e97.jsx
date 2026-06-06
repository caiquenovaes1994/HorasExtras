
import {Fragment,memo,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {Badge as RadixThemesBadge,Button as RadixThemesButton,Flex as RadixThemesFlex,Table as RadixThemesTable} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Foreach_comp_16ff824c010b77be7eccb7dd5b6b2e97 = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_hoteis____hotel_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_hoteis____hotel_state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.solicitacoes_rx_state_ ?? [],((s_rx_state_,index_2b6798d597ac3d47f086c35ce1eee7da)=>(jsx(RadixThemesTable.Row,{key:index_2b6798d597ac3d47f086c35ce1eee7da},jsx(RadixThemesTable.Cell,{},jsx(RadixThemesBadge,{color:"orange"},s_rx_state_?.["tipo"])),jsx(RadixThemesTable.Cell,{},s_rx_state_?.["rid"]),jsx(RadixThemesTable.Cell,{},s_rx_state_?.["nome"]),jsx(RadixThemesTable.Cell,{},s_rx_state_?.["user_id"]),jsx(RadixThemesTable.Cell,{align:"right"},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",justify:"end",gap:"2"},jsx(RadixThemesButton,{css:({ ["cursor"] : "pointer" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_hoteis____hotel_state.approve_solicitacao", ({ ["req_id"] : s_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\u2705"),jsx(RadixThemesButton,{css:({ ["cursor"] : "pointer" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_hoteis____hotel_state.reject_solicitacao", ({ ["req_id"] : s_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\u274c")))))))
    )
});
